import json
from pathlib import Path
from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

try:
    from . import clause_classifier, clause_risk_scorer, compliance_checker, entity_extraction
    from .ocr_services import extract_text
except ImportError:
    import clause_classifier  # type: ignore
    import clause_risk_scorer  # type: ignore
    import compliance_checker  # type: ignore
    import entity_extraction  # type: ignore
    from ocr_services import extract_text  # type: ignore

router = APIRouter()

DATA_DIR = Path(__file__).resolve().parent / "data"
MAX_ANALYZE_CHARS = 12000


class AnalyzeRequest(BaseModel):
    text: str


class AnalyzeFileRequest(BaseModel):
    filename: str


def _try_parse_json(raw: Any, fallback: dict[str, Any]) -> dict[str, Any]:
    if isinstance(raw, dict):
        return raw
    if not isinstance(raw, str):
        return fallback

    candidate = raw.strip()
    if candidate.startswith("```"):
        candidate = candidate.strip("`")
        if candidate.startswith("json"):
            candidate = candidate[4:].strip()

    try:
        parsed = json.loads(candidate)
        return parsed if isinstance(parsed, dict) else fallback
    except json.JSONDecodeError:
        start = candidate.find("{")
        end = candidate.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                parsed = json.loads(candidate[start : end + 1])
                return parsed if isinstance(parsed, dict) else fallback
            except json.JSONDecodeError:
                return fallback
        return fallback


def _run_analysis(clause_text: str) -> dict[str, Any]:
    text_for_analysis = clause_text[:MAX_ANALYZE_CHARS]

    entities = entity_extraction.extract_entities(text_for_analysis)
    entity_labels = [item["text"] for item in entities]

    raw_type = clause_classifier.classify_clause(text_for_analysis)
    clause_type_data = _try_parse_json(raw_type, {"type": "General"})

    raw_risk = clause_risk_scorer.score_risk(text_for_analysis)
    risk_data = _try_parse_json(
        raw_risk,
        {"risk": "Medium", "score": 50, "reason": "Unable to parse risk output"},
    )

    raw_compliance = compliance_checker.check_compliance(text_for_analysis)
    compliance_data = _try_parse_json(
        raw_compliance,
        {"compliant": True, "violations": [], "recommendations": []},
    )

    return {
        "entities": entity_labels,
        "entity_details": entities,
        "clause_type": clause_type_data.get("type", "General"),
        "risk": risk_data.get("risk", "Medium"),
        "risk_score": risk_data.get("score", 50),
        "risk_reason": risk_data.get("reason", "No reason provided"),
        "compliance": bool(compliance_data.get("compliant", True)),
        "compliance_issues": compliance_data.get("violations", []),
        "recommendations": compliance_data.get("recommendations", []),
    }


@router.post("/")
async def analyze_text(request: Optional[AnalyzeRequest] = None, text: Optional[str] = Query(default=None)):
    clause_text = request.text if request else text
    if not clause_text or not clause_text.strip():
        raise HTTPException(status_code=400, detail="text is required")
    return _run_analysis(clause_text)


@router.post("/file/")
async def analyze_file(request: AnalyzeFileRequest):
    safe_filename = Path(request.filename).name
    if not safe_filename:
        raise HTTPException(status_code=400, detail="filename is required")

    file_path = DATA_DIR / safe_filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {safe_filename}")

    try:
        document_text = extract_text(str(file_path))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to extract text from file: {exc}") from exc

    if not document_text or not document_text.strip():
        raise HTTPException(status_code=422, detail="No readable text extracted from document")

    result = _run_analysis(document_text)
    result["filename"] = safe_filename
    result["analyzed_chars"] = min(len(document_text), MAX_ANALYZE_CHARS)
    result["total_chars"] = len(document_text)
    return result
