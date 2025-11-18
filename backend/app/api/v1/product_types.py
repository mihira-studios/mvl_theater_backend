
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...deps import get_db
from ...models.product_types import ProductType
from ...schemas.product_types import ProductTypeOut, ProductTypeCreate

router = APIRouter()

@router.get("/", response_model=List[ProductTypeOut])
def list_product_types(db: Session = Depends(get_db)):
    return db.query(ProductType).all()

@router.post("/", response_model=ProductTypeOut)
def create_product_type(payload: ProductTypeCreate, db: Session = Depends(get_db)):
    pt = ProductType(
        name=payload.name,
        family=payload.family,
        scope=payload.scope,
    )
    db.add(pt)
    db.commit()
    db.refresh(pt)
    return pt
