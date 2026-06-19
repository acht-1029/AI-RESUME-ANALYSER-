"""
PDF Text Extractor
==================
Extracts raw text from resume PDFs using PyMuPDF (fitz).
Handles multi-page documents, returns clean concatenated text.
"""

import logging
from pathlib import Path

# pyrefly: ignore [missing-import]
import fitz  # PyMuPDF

logger = logging.getLogger(__name__)


def extract_text(pdf_path: str) -> str:
    """
    Extract all text from a PDF file.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        Cleaned, concatenated text from all pages.

    Raises:
        FileNotFoundError: If the PDF file does not exist.
        ValueError: If the file is not a PDF or contains no extractable text.
    """
    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a .pdf file, got: {path.suffix}")

    try:
        doc = fitz.open(str(path))
    except Exception as e:
        raise ValueError(f"Cannot open PDF (corrupt or encrypted?): {e}")

    pages_text = []
    for page_num, page in enumerate(doc):
        text = page.get_text("text")
        if text.strip():
            pages_text.append(text)
        else:
            logger.warning(f"Page {page_num + 1} has no extractable text (may be image-only).")

    doc.close()

    if not pages_text:
        raise ValueError(
            "No text could be extracted from the PDF. "
            "It may be a scanned/image-only document."
        )

    # Join pages, normalize whitespace
    raw_text = "\n".join(pages_text)
    # Collapse multiple blank lines into one
    lines = raw_text.splitlines()
    cleaned_lines = []
    prev_blank = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if not prev_blank:
                cleaned_lines.append("")
            prev_blank = True
        else:
            cleaned_lines.append(stripped)
            prev_blank = False

    cleaned_text = "\n".join(cleaned_lines).strip()
    logger.info(f"Extracted {len(cleaned_text)} chars from {len(pages_text)} page(s).")
    return cleaned_text


def extract_text_safe(pdf_path: str) -> dict:
    """
    Safe wrapper that never raises — returns error info instead.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        dict with keys:
            - "success": bool
            - "text": str (extracted text, or empty on failure)
            - "error": str or None
            - "page_count": int
    """
    try:
        text = extract_text(pdf_path)
        doc = fitz.open(str(pdf_path))
        page_count = len(doc)
        doc.close()
        return {
            "success": True,
            "text": text,
            "error": None,
            "page_count": page_count,
        }
    except Exception as e:
        logger.error(f"PDF extraction failed: {e}")
        return {
            "success": False,
            "text": "",
            "error": str(e),
            "page_count": 0,
        }
