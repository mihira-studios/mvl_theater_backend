"""
app/api/v1/script_breakdown.py
FastAPI router for the script breakdown feature.
Registered in app/api/v1/__init__.py under prefix /script.

Full endpoint: POST /api/v1/script/parse
"""

import tempfile
import os

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.schemas.script_breakdown import ScriptBreakdownResponse
from app.core.script_parser import ScriptParser


router = APIRouter()


@router.post(
    "/parse",
    response_model=ScriptBreakdownResponse,
    summary="Parse a screenplay PDF",
    description=(
        "Upload a PDF screenplay and receive a full breakdown: "
        "scene count, character count, scene list, and character appearances per scene."
    ),
)
async def parse_script(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    tmp_path = None
    try:
        # Save uploaded file to a temp location for pdfplumber to read
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        parser = ScriptParser(tmp_path)

        if not parser.extract_text():
            raise HTTPException(
                status_code=422,
                detail=(
                    f"Could not extract text from PDF. "
                    f"Ensure it is a text-based PDF, not a scanned image. "
                    f"Error: {parser.error}"
                )
            )

        parser.parse()
        return parser.get_results()

    finally:
        # Always clean up temp file regardless of success or failure
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)