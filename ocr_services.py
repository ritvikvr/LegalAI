from pathlib import Path

import pdfplumber
import pytesseract
from PIL import Image

try:
    from docx import Document
except Exception:
    Document = None


def _read_pdf(path: Path) -> str:
    text_parts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text_parts.append(page.extract_text() or "")
    return "\n".join(text_parts)


def _read_docx(path: Path) -> str:
    if Document is None:
        raise ValueError("DOCX support requires python-docx")
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def extract_text(path: str) -> str:
    source = Path(path)
    suffix = source.suffix.lower()

    if suffix == ".pdf":
        return _read_pdf(source)
    if suffix == ".txt":
        return source.read_text(encoding="utf-8", errors="ignore")
    if suffix == ".docx":
        return _read_docx(source)
    if suffix in {".png", ".jpg", ".jpeg", ".tiff", ".bmp"}:
        return pytesseract.image_to_string(Image.open(source))

    raise ValueError(f"Unsupported file type: {suffix}")
