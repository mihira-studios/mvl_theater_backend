
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Optional, Dict, Any
from .versions import VersionCreate



class ShotMini(BaseModel):
    id: UUID
    code: str
    name: Optional[str] = None
    status: str

class ProductCreateInline(BaseModel):
    project_id: UUID
    asset_id: Optional[UUID] = None
    shot_id: Optional[UUID] = None
    task_id: Optional[UUID] = None
    product_type_id: UUID

    name: str
    status: str = "active"
    user_id: UUID

    # include only if your Product model actually has meta
    meta: Optional[Dict[str, Any]] = None

class AssetBootstrapCreateMinimal(BaseModel):
    # ---- required (identity + ownership) ----
    project_id: UUID
    user_id: UUID

    asset_category: str   # e.g. "Vehicle", "Character"
    asset_type: str       # e.g. "Car", "Hero"

    asset_code: str       # e.g. "AST_001"
    asset_name: str       # e.g. "Hero Car"

    # ---- required (first publish) ----
    path: str             # main usd path/key
    thumbnail_path: str   # thumbnail path/key

    # ---- optional (sane defaults) ----
    asset_status: str = "active"
    product_status: str = "active"
    version_status: str = "draft"

    product_type: str = "model"   # e.g. "model", "rig", "lookdev"
    notes: Optional[str] = None

    # optional metadata buckets
    asset_meta: Optional[Dict[str, Any]] = None
    product_meta: Optional[Dict[str, Any]] = None
    version_meta: Optional[Dict[str, Any]] = None

    # optional overrides
    ext: str = "usd"
    thumbnail_ext: str = "jpg"
    thumbnail_metadata: Optional[Dict[str, Any]] = None

class AssetCreateWithProductAndVersion(BaseModel):
    # asset fields (same as AssetCreate)
    project_id: UUID
    asset_category_id: UUID
    asset_type_id: UUID
    code: str
    name: str
    status: str = "active"
    meta: Optional[Dict[str, Any]] = None

    product: ProductCreateInline
    version: VersionCreate

class AssetCreate(BaseModel):
    project_id: UUID
    asset_category_id: UUID
    asset_type_id: UUID
    code: Optional[str] = None
    name: str = None
    status: str = "new"
    meta: Dict[str, Any] = {}
    shot_ids: list[UUID] = []

class AssetOut(BaseModel):
    # ... your existing fields ...
    id: UUID
    project_id: UUID
    asset_category_id: UUID
    asset_type_id: UUID
    code: str
    name: str
    status: str
    meta: Optional[dict] = None

    # new convenience fields
    path: Optional[str] = None
    thumbnail_path: Optional[str] = None
    shots: list[ShotMini] = []

    created_at: datetime

    class Config:
        from_attributes = True

class AssetFromCSV(BaseModel):
    name: str
    status: str | None = None
    meta: dict

class AssetUpdate(BaseModel):
    # -------------------------
    # Asset core fields
    # -------------------------
    name: Optional[str] = None
    code: Optional[str] = None
    status: Optional[str] = None

    # allow updating category/type by *name*
    asset_category: Optional[str] = None
    asset_type: Optional[str] = None

    # partial merge into Asset.meta
    meta: Optional[Dict[str, Any]] = None


    # -------------------------
    # Media / Version fields
    # (if any of these are present, we update latest Version
    #  or create Product+Version if none exist)
    # -------------------------
    path: Optional[str] = None            # can be URL, s3 key, local path
    ext: Optional[str] = None            # "fbx", "uasset", "png", etc.

    thumbnail_path: Optional[str] = None # URL or s3 key
    thumbnail_ext: Optional[str] = None  # "jpg"/"png"
    thumbnail_metadata: Optional[Dict[str, Any]] = None


    # -------------------------
    # Needed when creating Product/Version on empty
    # -------------------------
    product_type: Optional[str] = None   # e.g. "model", "rig"
    product_status: Optional[str] = None # default "wip" in handler

    version_status: Optional[str] = None # default "wip" in handler
    notes: Optional[str] = None          # goes to Version.notes

    # who is making this update (required if creating product/version)
    user_id: Optional[UUID] = None


    # -------------------------
    # Optional tags for Version
    # -------------------------
    tags: Optional[Dict[str, Any]] = None

    shot_ids: Optional[list[UUID]] = None  # None=no change, []=clear all


    class Config:
        extra = "forbid"  # reject unknown fields to catch typos early

