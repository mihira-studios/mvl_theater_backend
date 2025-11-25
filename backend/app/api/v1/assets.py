import csv
from pathlib import Path
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ...deps import get_db
from ...models.assets import Asset
from ...models.products import Product
from ...models.versions import Version
from ...schemas.assets import (
    AssetOut,
    AssetFromCSV,
    AssetCreateWithProductAndVersion,
    AssetBootstrapCreateMinimal,
)
from ...core.resolver import (
    resolve_asset_type_id,
    resolve_asset_category_id,
    resolve_product_type_id,
)
from ...schemas.versions import VersionOut

from ...core.s3 import (
    create_presigned_upload_url,
    create_presigned_download_url,
    S3_BUCKET,
)

router = APIRouter()

CSV_ASSETS_PATH = Path("/mnt/bb3/Asset.csv")


@router.get("/", response_model=List[AssetOut])
def list_assets(
    project_id: UUID | None = None,
    db: Session = Depends(get_db),
):
    q = db.query(Asset)
    if project_id:
        q = q.filter(Asset.project_id == project_id)
    return q.order_by(Asset.created_at.desc()).all()


@router.post("/", response_model=AssetOut)
def create_asset(payload: AssetBootstrapCreateMinimal, db: Session = Depends(get_db)):
    """
    Flat payload -> Asset -> Product -> Version.
    IDs resolved by name, version auto-incremented.
    """
    try:
        # ---- resolve lookup ids ----
        asset_category_id = resolve_asset_category_id(
            db, payload.project_id, payload.asset_category
        )
        asset_type_id = resolve_asset_type_id(
            db, payload.project_id, asset_category_id, payload.asset_type
        )
        product_type_id = resolve_product_type_id(
            db, payload.project_id, payload.product_type
        )

        # ---- 1) create Asset ----
        asset = Asset(
            project_id=payload.project_id,
            asset_category_id=asset_category_id,
            asset_type_id=asset_type_id,
            code=payload.asset_code,
            name=payload.asset_name,
            status=payload.asset_status,
            meta=payload.asset_meta,
        )
        db.add(asset)
        db.flush()  # asset.id now available

        # ---- 2) create Product ----
        product = Product(
            project_id=payload.project_id,
            asset_id=asset.id,
            product_type_id=product_type_id,
            name=payload.asset_name if payload.product_type == "model" else f"{payload.asset_name} - {payload.product_type}",
            status=payload.product_status,
            user_id=payload.user_id,
            meta=payload.product_meta,
        )
        db.add(product)
        db.flush()

        # ---- 3) create Version (auto number) ----
        ver_num = next_version_number(db, product.id)

        ver = Version(
            product_id=product.id,
            version=ver_num,
            status=payload.version_status,
            notes=payload.notes,
            user_id=payload.user_id,

            path=payload.path,
            ext=payload.ext,
            meta=payload.version_meta,

            thumbnail_path=payload.thumbnail_path,
            thumbnail_ext=payload.thumbnail_ext,
            thumbnail_metadata=payload.thumbnail_metadata,

            tags=payload.tags.dict() if payload.tags else None,
        )
        db.add(ver)

        db.commit()
        db.refresh(asset)
        return asset

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to bootstrap asset: {e}")


@router.get("/{asset_id}", response_model=AssetOut)
def get_asset_detail(
    asset_id: UUID,
    db: Session = Depends(get_db),
):
    asset = _get_asset_or_404(db, asset_id)
    asset_out = AssetOut.from_orm(asset)

    asset_out.path = None
    asset_out.thumbnail_path = None

    latest_version = (
        db.query(Version)
        .join(Product, Product.id == Version.product_id)
        .filter(Product.asset_id == asset_id)
        .order_by(Version.created_at.desc())
        .first()
    )

    if latest_version:
        asset_out.path = latest_version.path
        asset_out.thumbnail_path = latest_version.thumbnail_path

    return asset_out


@router.get("/{asset_id}/versions", response_model=List[VersionOut])
def list_asset_versions(
    asset_id: UUID,
    db: Session = Depends(get_db),
):
    _get_asset_or_404(db, asset_id)

    versions = (
        db.query(Version)
        .join(Product, Product.id == Version.product_id)
        .filter(Product.asset_id == asset_id)
        .order_by(Version.created_at.desc())
        .all()
    )
    return versions


@router.get("/from_csv", response_model=List[AssetFromCSV])
def list_assets_from_csv():
    if not CSV_ASSETS_PATH.exists():
        print("file not found:", CSV_ASSETS_PATH)
        raise HTTPException(status_code=500, detail="Assets CSV file not found")

    assets: List[AssetFromCSV] = []

    try:
        with CSV_ASSETS_PATH.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for raw_row in reader:
                row = {
                    k.strip().lower().replace(" ", "_"): (v.strip() if isinstance(v, str) else v)
                    for k, v in raw_row.items()
                }

                asset_name = row.get("asset_name") or row.get("asset") or "Unnamed asset"
                status = row.get("status") or "unknown"

                meta = {
                    "type": row.get("type"),
                    "category": row.get("category"),
                    "thumbnail": row.get("thumbnail"),
                    "description": row.get("description"),
                    "project": row.get("project"),
                    "source": "csv_import",
                }

                assets.append(AssetFromCSV(
                    name=asset_name,
                    status=status,
                    meta=meta,
                ))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read assets CSV: {e}")

    return assets


class AssetUploadInit(BaseModel):
    filename: str
    content_type: str | None = None


class PresignedUrlOut(BaseModel):
    url: str
    key: str
    bucket: str


def _get_asset_or_404(db: Session, asset_id: UUID) -> Asset:
    asset = db.query(Asset).get(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.post("/{asset_id}/upload_url", response_model=PresignedUrlOut)
def get_asset_upload_url(
    asset_id: UUID,
    payload: AssetUploadInit,
    db: Session = Depends(get_db),
):
    asset = _get_asset_or_404(db, asset_id)

    key = f"assets/{asset_id}/{payload.filename}"

    meta = asset.meta or {}
    meta["file_key"] = key
    meta["filename"] = payload.filename
    if payload.content_type:
        meta["content_type"] = payload.content_type
    asset.meta = meta

    db.add(asset)
    db.commit()
    db.refresh(asset)

    url = create_presigned_upload_url(key)
    return PresignedUrlOut(url=url, key=key, bucket=S3_BUCKET)


@router.get("/{asset_id}/download_url", response_model=PresignedUrlOut)
def get_asset_download_url(
    asset_id: UUID,
    db: Session = Depends(get_db),
):
    asset = _get_asset_or_404(db, asset_id)

    meta = asset.meta or {}
    file_key = meta.get("file_key")
    if not file_key:
        raise HTTPException(status_code=400, detail="Asset has no file_key in meta")

    url = create_presigned_download_url(file_key)
    return PresignedUrlOut(url=url, key=file_key, bucket=S3_BUCKET)
