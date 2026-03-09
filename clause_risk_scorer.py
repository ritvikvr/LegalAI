import json
import os
from functools import lru_cache

try:
    from langchain.prompts import PromptTemplate
    from langchain_openai import ChatOpenAI
except Exception:
    PromptTemplate = None
    ChatOpenAI = None

HIGH_RISK_TERMS = {
    "unlimited liability",
    "sole discretion",
    "without notice",
    "irrevocable",
    "non-refundable",
}

MEDIUM_RISK_TERMS = {
    "indemnify",
    "arbitration",
    "termination for convenience",
    "penalty",
}


@lru_cache(maxsize=1)
def _get_llm():
    if PromptTemplate is None or ChatOpenAI is None:
        return None, None
    if not os.getenv("OPENAI_API_KEY"):
        return None, None
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = PromptTemplate(
        input_variables=["clause"],
        template="""
Assess risk level (High, Medium, Low) for this clause.

Clause:
{clause}

Return JSON:
{{"risk":"High|Medium|Low","score":0-100,"reason":""}}
""",
    )
    return llm, prompt


def _fallback_score(clause: str) -> str:
    text = clause.lower()
    high_hits = [term for term in HIGH_RISK_TERMS if term in text]
    medium_hits = [term for term in MEDIUM_RISK_TERMS if term in text]
    if high_hits:
        return json.dumps(
            {
                "risk": "High",
                "score": 82,
                "reason": f"Found high-risk terms: {', '.join(high_hits)}",
            }
        )
    if medium_hits:
        return json.dumps(
            {
                "risk": "Medium",
                "score": 58,
                "reason": f"Found medium-risk terms: {', '.join(medium_hits)}",
            }
        )
    return json.dumps({"risk": "Low", "score": 25, "reason": "No explicit high-risk terms detected"})


def score_risk(clause: str) -> str:
    llm, prompt = _get_llm()
    if llm is None or prompt is None:
        return _fallback_score(clause)
    return llm.invoke(prompt.format(clause=clause[:3000])).content
