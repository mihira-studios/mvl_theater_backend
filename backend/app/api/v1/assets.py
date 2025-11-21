from typing import List
from uuid import UUID

import csv
import json
from pathlib import Path
from typing import List
from uuid import UUID


from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ...deps import get_db
from ...models.assets import Asset
from ...schemas.assets import AssetOut, AssetCreate, AssetFromCSV
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
def create_asset(payload: AssetCreate, db: Session = Depends(get_db)):
    asset = Asset(
        project_id=payload.project_id,
        asset_category_id=payload.asset_category_id,
        asset_type_id=payload.asset_type_id,
        code=payload.code,
        name=payload.name,
        status=payload.status,
        meta=payload.meta,
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


@router.get("/from_csv", response_model=List[AssetFromCSV])
def list_assets_from_csv():
    """
    Read assets from a CSV file and return them as AssetOut models.

    Expected CSV columns:
    - type
    - category
    - asset name
    - thumbnai (thumbnail)
    - status
    - description
    - Project
    """

    if not CSV_ASSETS_PATH.exists():
        print(f"file not found:", CSV_ASSETS_PATH)
        raise HTTPException(status_code=500, detail="Assets CSV file not found")

    assets: List[AsssetFromCSV] = []

    try:
        with CSV_ASSETS_PATH.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for raw_row in reader:
                # --- normalize keys: "asset name" -> "asset_name", "thumbnai" -> "thumbnai" etc. ---
                row = {k.strip().lower().replace(" ", "_"): (v.strip() if isinstance(v, str) else v)
                       for k, v in raw_row.items()}

                # Expected normalized keys:
                # type, category, asset_name, thumbnai, status, description, project


                asset_name = row.get("asset_name") or row.get("asset") or "Unnamed asset"
                status = row.get("status") or "unknown"

                # Project column might be a UUID or some other identifier.
                # If it's NOT a UUID in your CSV, remove this block and just keep it in meta.
                project_id = None
                project_raw = row.get("project")
                if project_raw:
                    try:
                        project_id = project_raw
                    except ValueError:
                        # Not a UUID – keep as plain string inside meta instead
                        project_id = None

                # Build meta from CSV columns (anything you want to keep)
                meta = {
                    "type": row.get("type"),
                    "category": row.get("category"),
                    "thumbnail": row.get("thumbnail"),
                    "description": row.get("description"),
                    "project": project_raw,
                    "source": "csv_import",
                }

                # Build a payload compatible with AssetOut.
                # Adapt this dict to match your actual AssetOut fields.
                asset_data = {
                    "name": asset_name,
                    "status": status,
                    "meta": meta,
                }

                # if "project_id" in AssetOut.model_fields:  # Pydantic v2
                #     asset_data["project_id"] = project_id

                # If AssetOut has required fields like id/created_at, either:
                # - make them optional in the schema, or
                # - add dummy values here.
                # Example (uncomment if needed):
                # from uuid import uuid4
                # asset_data["id"] = uuid4()

                assets.append(AssetFromCSV(**asset_data))
               

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

    # Example key: assets/<asset_id>/<filename>
    key = f"assets/{asset_id}/{payload.filename}"

    # Update asset.meta
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
