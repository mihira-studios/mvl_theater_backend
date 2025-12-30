from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...deps import get_db
from ...models.products import Product
from ...models.versions import Version
from ...schemas.products import ProductOut, ProductCreateWithVersion

router = APIRouter()


@router.get("/", response_model=List[ProductOut])
def list_products(
    project_id: UUID | None = None,
    owner_kind: str | None = None,
    owner_id: UUID | None = None,
    db: Session = Depends(get_db),
):
    q = db.query(Product)

    if project_id:
        q = q.filter(Product.project_id == project_id)

    if owner_kind:
        q = q.filter(Product.owner_kind == owner_kind)

    if owner_id:
        q = q.filter(Product.owner_id == owner_id)

    return q.order_by(Product.created_at.desc()).all()


@router.post("/", response_model=ProductOut)
def create_product(payload: ProductCreateWithVersion, db: Session = Depends(get_db)):
    try:
        # --- basic validation of owner_kind ---
        if payload.owner_kind not in ("asset", "shot", "task"):
            raise HTTPException(status_code=400, detail="owner_kind must be asset|shot|task")

        # --- 1) create Product ---
        prod = Product(
            project_id=payload.project_id,
            owner_kind=payload.owner_kind,
            owner_id=payload.owner_id,
            product_type_id=payload.product_type_id,
            status=payload.status or "draft",
            created_by=payload.created_by,
        )
        db.add(prod)
        db.flush()  # prod.id ready

        # --- 2) create first Version ---
        v = payload.version
        ver = Version(
            product_id=prod.id,
            version=1,

            status=v.status or "wip",
            notes=v.notes,
            user_id=v.user_id,

            path=v.path,
            ext=v.ext,
            meta=v.meta,

            thumbnail_path=v.thumbnail_path,
            thumbnail_ext=v.thumbnail_ext,
            thumbnail_metadata=v.thumbnail_metadata,

            tags=v.tags if v.tags else None,
        )
        db.add(ver)

        db.commit()
        db.refresh(prod)
        return prod

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
