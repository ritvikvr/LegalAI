import re
from functools import lru_cache
from typing import Dict, List

import spacy

_DATE_PATTERNS = (
    r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
    r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b",
)
_MONEY_PATTERNS = (
    r"\b(?:USD|INR|EUR|GBP)\s?\d[\d,]*(?:\.\d+)?\b",
    r"(?:\$|₹|Rs\.?)\s?\d[\d,]*(?:\.\d+)?",
)
_ORG_PATTERN = (
    r"\b[A-Z][A-Za-z0-9&'\-]*(?:\s+[A-Z][A-Za-z0-9&'\-]*){0,5}\s+"
    r"(?:Pvt\.?\s?Ltd\.?|Ltd\.?|Limited|LLC|Inc\.?|Corporation|Corp\.?|LLP)\b"
)
_PARTY_PATTERN = r"\b(?:Party\s+[A-Z]|First Party|Second Party|Client|Vendor|Supplier|Employer|Employee)\b"
_EMAIL_PATTERN = r"\b[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[A-Za-z]{2,}\b"


@lru_cache(maxsize=1)
def _get_nlp():
    for model_name in ("en_core_web_trf", "en_core_web_sm"):
        try:
            return spacy.load(model_name)
        except Exception:
            continue
    return spacy.blank("en")


def _append_unique(results: List[Dict[str, str]], seen: set, text: str, label: str):
    cleaned = " ".join(text.strip().split())
    if label == "ORG":
        cleaned = re.sub(r"^(?:AND|And|and)\s+", "", cleaned)
    if not cleaned:
        return
    key = (cleaned.lower(), label)
    if key in seen:
        return
    seen.add(key)
    results.append({"text": cleaned, "label": label})


def _regex_entities(text: str) -> List[Dict[str, str]]:
    found: List[Dict[str, str]] = []
    seen = set()

    for pattern in _DATE_PATTERNS:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            _append_unique(found, seen, match.group(0), "DATE")

    for pattern in _MONEY_PATTERNS:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            _append_unique(found, seen, match.group(0), "MONEY")

    for match in re.finditer(_ORG_PATTERN, text):
        _append_unique(found, seen, match.group(0), "ORG")

    for match in re.finditer(_PARTY_PATTERN, text, flags=re.IGNORECASE):
        _append_unique(found, seen, match.group(0), "PARTY")

    for match in re.finditer(_EMAIL_PATTERN, text):
        _append_unique(found, seen, match.group(0), "EMAIL")

    return found


def extract_entities(text: str):
    results: List[Dict[str, str]] = []
    seen = set()

    doc = _get_nlp()(text)
    for ent in doc.ents:
        label = ent.label_ or "ENTITY"
        _append_unique(results, seen, ent.text, label)

    for item in _regex_entities(text):
        _append_unique(results, seen, item["text"], item["label"])

    return results
