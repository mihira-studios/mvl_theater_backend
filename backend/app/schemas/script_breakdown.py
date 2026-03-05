"""
app/schemas/script_breakdown.py
Pydantic response schema for the script breakdown endpoint.
"""

from pydantic import BaseModel
from typing import Dict, List


class ScriptBreakdownResponse(BaseModel):
    total_pages: int
    total_scenes: int
    total_characters: int
    scenes: List[str]
    characters: List[str]
    character_appearances: Dict[str, int]
    character_scenes: Dict[str, List[str]]