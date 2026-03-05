"""
app/core/script_parser.py
Core parsing logic — no UI, no API. Just pure extraction.
Called directly by the FastAPI endpoint.
"""

import re
from collections import defaultdict
from typing import Optional
import pdfplumber


# ---------------------------------------------------------------------------
# Regex Patterns
# ---------------------------------------------------------------------------

SCENE_PATTERN = re.compile(
    r'^\s*(INT\.|EXT\.|INT\/EXT\.|I\/E\.)',
    re.IGNORECASE
)

# Handles both indented (standard) and flush-left screenplay formats
CHARACTER_PATTERN = re.compile(
    r'^[ \t]{0,}([A-Z][A-Z0-9\s\'\-\.]{1,40}?)(\s*\(.*?\))?\s*$'
)

FALSE_POSITIVE_KEYWORDS = {
    'CUT TO', 'FADE IN', 'FADE OUT', 'FADE TO', 'DISSOLVE TO',
    'SMASH CUT', 'MATCH CUT', 'TITLE CARD', 'SUPER', 'THE END',
    'CONTINUED', 'MORE', 'INTERCUT', 'BACK TO', 'FLASH CUT',
    'TIME CUT', 'END OF', 'ACT ONE', 'ACT TWO', 'ACT THREE',
    'COLD OPEN', 'TAG', 'TEASER', 'EPILOGUE', 'PROLOGUE',
    'FADE', 'INT', 'EXT', 'SOUND', 'NOTE', 'TITLE', 'SERIES',
    'LATER', 'CONTINUOUS', 'MOMENTS', 'MEANWHILE'
}


# ---------------------------------------------------------------------------
# Parser Class
# ---------------------------------------------------------------------------

class ScriptParser:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.raw_lines = []
        self.scenes = []
        self.characters = set()
        self.character_appearances = {}
        self.character_scenes = defaultdict(set)  # name -> set of scenes appeared in
        self.total_pages = 0
        self.error: Optional[str] = None

    def extract_text(self) -> bool:
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                self.total_pages = len(pdf.pages)
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        self.raw_lines.extend(text.splitlines())
            return True
        except Exception as e:
            self.error = str(e)
            return False

    def _clean_character_name(self, name: str) -> str:
        name = re.sub(r'\(.*?\)', '', name)
        return name.strip()

    def _is_false_positive(self, name: str) -> bool:
        name_upper = name.upper().strip()
        for keyword in FALSE_POSITIVE_KEYWORDS:
            if keyword in name_upper:
                return True
        return len(name_upper) < 2

    def _is_dialogue_or_parenthetical(self, line: str) -> bool:
        """Confirms preceding line was a character cue by checking next line is dialogue."""
        stripped = line.strip()
        if not stripped:
            return False
        if stripped.startswith('(') and stripped.endswith(')'):
            return True
        if not stripped.isupper() and len(stripped) > 2:
            return True
        return False

    def parse(self):
        current_scene = None

        for i, line in enumerate(self.raw_lines):
            stripped = line.strip()

            # Scene detection — track current scene context
            if SCENE_PATTERN.match(line):
                current_scene = stripped
                self.scenes.append(current_scene)
                continue

            # Character detection — ALL CAPS line followed by dialogue
            match = CHARACTER_PATTERN.match(line)
            if match and stripped.isupper():
                # Peek ahead to confirm next line is dialogue/parenthetical
                next_line = ""
                for j in range(i + 1, min(i + 3, len(self.raw_lines))):
                    if self.raw_lines[j].strip():
                        next_line = self.raw_lines[j]
                        break

                if self._is_dialogue_or_parenthetical(next_line):
                    name = self._clean_character_name(match.group(1))
                    if name and not self._is_false_positive(name):
                        self.characters.add(name)
                        # Add to scene set — duplicates ignored automatically
                        if current_scene:
                            self.character_scenes[name].add(current_scene)

        # Build appearances: unique scene count per character, sorted descending
        self.character_appearances = dict(
            sorted(
                {name: len(scenes) for name, scenes in self.character_scenes.items()}.items(),
                key=lambda x: -x[1]
            )
        )

    def get_results(self) -> dict:
        return {
            "total_pages": self.total_pages,
            "total_scenes": len(self.scenes),
            "total_characters": len(self.characters),
            "scenes": self.scenes,
            "characters": sorted(self.characters),
            "character_appearances": self.character_appearances,
            "character_scenes": {
                name: sorted(list(scenes))
                for name, scenes in self.character_scenes.items()
            }
        }