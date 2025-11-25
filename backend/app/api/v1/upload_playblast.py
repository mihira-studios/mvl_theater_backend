from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session
from db import get_db
from services.version import attach_playblast_to_version
from schemas.version import VersionOut

router = APIRouter(prefix="/versions", tags=["Versions"])


@router.post("/{version_id}/playblast", response_model=VersionOut)
async def upload_playblast(
    version_id: str,
    file: UploadFile,
    db: Session = Depends(get_db)
):
    version = attach_playblast_to_version(db, version_id, file)
    return version
