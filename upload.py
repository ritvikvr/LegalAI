from pathlib import Path
import shutil

from fastapi import APIRouter, File, HTTPException, UploadFile

try:
    from .chunker import chunk_text
    from .embedding_service import embed
    from .ocr_services import extract_text
    from .vector_store import add_embeddings
except ImportError:
    from chunker import chunk_text  # type: ignore
    from embedding_service import embed  # type: ignore
    from ocr_services import extract_text  # type: ignore
    from vector_store import add_embeddings  # type: ignore

router = APIRouter()
DATA_DIR = Path(__file__).resolve().parent / "data"
ALLOWED_SUFFIXES = {".pdf", ".txt", ".docx", ".png", ".jpg", ".jpeg", ".tiff", ".bmp"}


@router.post("/")
async def upload(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="File name is missing")

    file_name = Path(file.filename).name
    suffix = Path(file_name).suffix.lower()
    if suffix not in ALLOWED_SUFFIXES:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {suffix}")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    file_path = DATA_DIR / file_name

    with file_path.open("wb") as out_file:
        shutil.copyfileobj(file.file, out_file)

    try:
        text = extract_text(str(file_path))
        if not text or not text.strip():
            raise HTTPException(status_code=422, detail="No readable text extracted from document")

        chunks = chunk_text(text)
        embeddings = embed(chunks)
        add_embeddings(embeddings, chunks)
        return {"status": "Indexed", "chunks": len(chunks), "filename": file_name}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Upload failed: {exc}") from exc
