import json
import os
from functools import lru_cache

try:
    from langchain_openai import ChatOpenAI
except Exception:
    ChatOpenAI = None


@lru_cache(maxsize=1)
def _get_llm():
    if ChatOpenAI is None:
        return None
    if not os.getenv("OPENAI_API_KEY"):
        return None
    return ChatOpenAI(model="gpt-4o-mini", temperature=0)


def _fallback_compliance(text: str) -> str:
    lower_text = text.lower()
    violations = []
    recommendations = []

    if "governing law" not in lower_text and "jurisdiction" not in lower_text:
        violations.append("Missing governing law or jurisdiction clause")
        recommendations.append("Add a governing law and jurisdiction clause")
    if "confidential" not in lower_text and "non-disclosure" not in lower_text:
        violations.append("Missing confidentiality commitment")
        recommendations.append("Add confidentiality / non-disclosure obligations")
    termination_tokens = ("termination", "terminate", "terminated")
    if not any(token in lower_text for token in termination_tokens):
        violations.append("Missing termination clause")
        recommendations.append("Define termination grounds and notice period")

    return json.dumps(
        {
            "compliant": len(violations) == 0,
            "violations": violations,
            "recommendations": recommendations,
        }
    )


def check_compliance(text: str) -> str:
    llm = _get_llm()
    if llm is None:
        return _fallback_compliance(text)

    prompt = f"""
Check compliance with Indian Contract Act & IT Act.

Document:
{text[:4000]}

Return strictly valid JSON with this shape:
{{
  "compliant": true/false,
  "violations": ["..."],
  "recommendations": ["..."]
}}
"""
    return llm.invoke(prompt).content
