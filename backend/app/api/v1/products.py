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
    db: Session = Depends(get_db),
):
    q = db.query(Product)
    if project_id:
        q = q.filter(Product.project_id == project_id)
    return q.order_by(Product.created_at.desc()).all()


@router.post("/", response_model=ProductOut)
def create_product(payload: ProductCreateWithVersion, db: Session = Depends(get_db)):
    try:
        prod = Product(
            project_id=payload.project_id,
            asset_id=payload.asset_id,
            shot_id=payload.shot_id,
            task_id=payload.task_id,
            product_type_id=payload.product_type_id,
            name=payload.name,
            status=payload.status,
            user_id=payload.user_id,
            meta=getattr(payload, "meta", None),
        )
        db.add(prod)
        db.flush()

        v = payload.version
        ver = Version(
            product_id=prod.id,
            version=1,  # first version always 1

            status=v.status,
            notes=v.notes,
            user_id=v.user_id,

            path=v.path,
            ext=v.ext,
            meta=v.meta,

            thumbnail_path=v.thumbnail_path,
            thumbnail_ext=v.thumbnail_ext,
            thumbnail_metadata=v.thumbnail_metadata,

            tags=v.tags.dict() if v.tags else None,
        )
        db.add(ver)

        db.commit()
        db.refresh(prod)
        return prod

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
