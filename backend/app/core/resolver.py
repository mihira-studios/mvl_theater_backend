from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models.asset_categories import AssetCategory
from ..models.asset_types import AssetType
from ..models.product_types import ProductType
from ..models.versions import Version


def _normalize_name(s: str) -> str:
    return s.strip().lower()


def resolve_asset_category_id(db: Session, project_id, name: str):
    n = _normalize_name(name)

    q = db.query(AssetCategory).filter(
        func.lower(AssetCategory.name) == n
    )

    # if your AssetCategory is project-scoped, prefer project match
    if hasattr(AssetCategory, "project_id"):
        q = q.filter(AssetCategory.project_id == project_id)

    cat = q.first()
    if not cat:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown asset_category '{name}'"
        )
    return cat.id


def resolve_asset_type_id(db: Session, project_id, category_id, name: str):
    n = _normalize_name(name)

    q = db.query(AssetType).filter(
        func.lower(AssetType.name) == n
    )

    # if asset types are category-scoped
    if hasattr(AssetType, "asset_category_id"):
        q = q.filter(AssetType.asset_category_id == category_id)

    # if project-scoped
    if hasattr(AssetType, "project_id"):
        q = q.filter(AssetType.project_id == project_id)

    t = q.first()
    if not t:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown asset_type '{name}' for category_id={category_id}"
        )
    return t.id


def resolve_product_type_id(db: Session, project_id, name: str):
    n = _normalize_name(name)

    q = db.query(ProductType).filter(
        func.lower(ProductType.name) == n
    )

    if hasattr(ProductType, "project_id"):
        q = q.filter(ProductType.project_id == project_id)

    pt = q.first()

    # if not found, fallback to default "model"
    if not pt:
        q2 = db.query(ProductType).filter(func.lower(ProductType.name) == "model")
        if hasattr(ProductType, "project_id"):
            q2 = q2.filter(ProductType.project_id == project_id)
        pt = q2.first()

    if not pt:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown product_type '{name}' and no default 'model' found"
        )
    return pt.id


def next_version_number(db: Session, product_id):
    max_ver = (
        db.query(func.max(Version.version))
        .filter(Version.product_id == product_id)
        .scalar()
    )
    return (max_ver or 0) + 1
