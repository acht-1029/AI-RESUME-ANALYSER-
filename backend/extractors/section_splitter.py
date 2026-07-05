"""
Resume Section Splitter
=======================
Splits raw resume text into named sections (education, experience, skills, etc.)
using regex-based header detection. Handles common resume formatting patterns.
"""

import re
import logging
from typing import Dict

logger = logging.getLogger(__name__)

# -------------------------------------------------------------------
# Section header patterns — order matters (first match wins)
# Each tuple: (canonical_name, compiled regex)
# -------------------------------------------------------------------
SECTION_PATTERNS = [
    ("summary", re.compile(
        r"^(?:professional\s+)?(?:summary|profile|objective|about\s*me|career\s+(?:summary|objective))\s*[:—\-]?\s*$",
        re.IGNORECASE,
    )),
    ("experience", re.compile(
        r"^(?:work\s+)?(?:experience|employment|professional\s+experience|work\s+history|career\s+history)\s*[:—\-]?\s*$",
        re.IGNORECASE,
    )),
    ("education", re.compile(
        r"^(?:education|academic|qualifications?|academic\s+background)\s*[:—\-]?\s*$",
        re.IGNORECASE,
    )),
    ("skills", re.compile(
        r"^(?:(?:technical\s+|key\s+|core\s+)?skills|competenc(?:ies|e)|technical\s+proficiency|technologies)\s*[:—\-]?\s*$",
        re.IGNORECASE,
    )),
    ("projects", re.compile(
        r"^(?:projects?|personal\s+projects?|academic\s+projects?|key\s+projects?)\s*[:—\-]?\s*$",
        re.IGNORECASE,
    )),
    ("certifications", re.compile(
        r"^(?:certifications?|licenses?\s*(?:&|and)?\s*certifications?|credentials?)\s*[:—\-]?\s*$",
        re.IGNORECASE,
    )),
    ("achievements", re.compile(
        r"^(?:achievements?|awards?|honors?|accomplishments?|recognitions?)\s*[:—\-]?\s*$",
        re.IGNORECASE,
    )),
    ("publications", re.compile(
        r"^(?:publications?|papers?|research)\s*[:—\-]?\s*$",
        re.IGNORECASE,
    )),
    ("languages", re.compile(
        r"^(?:languages?)\s*[:—\-]?\s*$",
        re.IGNORECASE,
    )),
    ("interests", re.compile(
        r"^(?:interests?|hobbies?|extracurricular)\s*[:—\-]?\s*$",
        re.IGNORECASE,
    )),
    ("contact", re.compile(
        r"^(?:contact\s*(?:info(?:rmation)?)?|personal\s+(?:info(?:rmation)?|details?))\s*[:—\-]?\s*$",
        re.IGNORECASE,
    )),
    ("references", re.compile(
        r"^(?:references?)\s*[:—\-]?\s*$",
        re.IGNORECASE,
    )),
]

# Heuristic: lines that look like section headers (ALL CAPS, short, etc.)
HEADER_HEURISTIC = re.compile(r"^[A-Z][A-Z\s&/,]{2,40}$")


def _classify_line(line: str) -> str | None:
    """Return canonical section name if `line` looks like a section header, else None."""
    cleaned = line.strip()
    if not cleaned or len(cleaned) > 60:
        return None

    # Try explicit patterns first
    for name, pattern in SECTION_PATTERNS:
        if pattern.match(cleaned):
            return name

    # Fallback: ALL-CAPS short line heuristic
    if HEADER_HEURISTIC.match(cleaned):
        lower = cleaned.lower().strip()
        # Try to match the lowercase version against our patterns
        for name, pattern in SECTION_PATTERNS:
            if pattern.match(lower):
                return name
        # Unknown section — still capture it
        logger.debug(f"Unknown section header detected: '{cleaned}'")
        return lower.replace(" ", "_")

    return None


def split_sections(text: str) -> Dict[str, str]:
    """
    Split resume text into named sections.

    Args:
        text: Raw resume text (from pdf_parser.extract_text).

    Returns:
        Dictionary mapping section names to their text content.
        Always includes a "header" key for content before the first section
        (usually the candidate's name/contact info).

    Example:
        {
            "header": "John Doe\\njohn@email.com\\n...",
            "summary": "Experienced developer...",
            "experience": "Company A — Software Engineer\\n...",
            "skills": "Python, Docker, AWS...",
            "education": "B.Tech in CS, XYZ University..."
        }
    """
    lines = text.splitlines()
    sections: Dict[str, str] = {}
    current_section = "header"
    current_lines: list[str] = []

    for line in lines:
        section_name = _classify_line(line)
        if section_name:
            # Save the previous section
            content = "\n".join(current_lines).strip()
            if content:
                # If we already have content for this section, append
                if current_section in sections:
                    sections[current_section] += "\n" + content
                else:
                    sections[current_section] = content
            # Start new section
            current_section = section_name
            current_lines = []
        else:
            current_lines.append(line)

    # Save the last section
    content = "\n".join(current_lines).strip()
    if content:
        if current_section in sections:
            sections[current_section] += "\n" + content
        else:
            sections[current_section] = content

    logger.info(f"Split resume into {len(sections)} sections: {list(sections.keys())}")
    return sections


def get_full_text_without_header(sections: Dict[str, str]) -> str:
    """
    Return all section content concatenated, excluding the header/contact info.
    Useful for similarity scoring where you don't want name/email affecting scores.
    """
    parts = []
    for key, value in sections.items():
        if key != "header":
            parts.append(value)
    return "\n".join(parts)
