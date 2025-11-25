
from fastapi import APIRouter
from . import (
    users,
    projects,
    access_groups,
    asset_categories,
    asset_types,
    sequences,
    assets,
    shots,
    tasks,
    product_types,
    products,
    versions,
)

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(access_groups.router, prefix="/access-groups", tags=["access-groups"])
api_router.include_router(asset_categories.router, prefix="/asset-categories", tags=["asset-categories"])
api_router.include_router(asset_types.router, prefix="/asset-types", tags=["asset-types"])
api_router.include_router(sequences.router, prefix="/sequences", tags=["sequences"])
api_router.include_router(assets.router, prefix="/assets", tags=["assets"])
api_router.include_router(shots.router, prefix="/shots", tags=["shots"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(product_types.router, prefix="/product-types", tags=["product-types"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(versions.router, prefix="/versions", tags=["versions"])
