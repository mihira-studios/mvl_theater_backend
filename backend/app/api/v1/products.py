
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...deps import get_db
from ...models.products import Product
from ...schemas.products import ProductOut, ProductCreate

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
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    prod = Product(
        project_id=payload.project_id,
        asset_id=payload.asset_id,
        shot_id=payload.shot_id,
        task_id=payload.task_id,
        product_type_id=payload.product_type_id,
        name=payload.name,
        status=payload.status,
        user_id=payload.user_id,
    )
    db.add(prod)
    db.commit()
    db.refresh(prod)
    return prod
