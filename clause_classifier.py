import json
import os
from functools import lru_cache

try:
    from langchain.prompts import PromptTemplate
    from langchain_openai import ChatOpenAI
except Exception:
    PromptTemplate = None
    ChatOpenAI = None

CLAUSE_KEYWORDS = {
    "Termination": ["terminate", "termination", "notice period"],
    "Confidentiality": ["confidential", "nda", "non-disclosure"],
    "Indemnity": ["indemnify", "indemnity", "hold harmless"],
    "Arbitration": ["arbitration", "arbitral", "dispute resolution"],
    "Governing Law": ["governing law", "jurisdiction", "courts of"],
    "Force Majeure": ["force majeure", "act of god"],
    "Payment": ["payment", "invoice", "fees", "consideration"],
    "Liability": ["liability", "damages", "limitation of liability"],
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
Classify this legal clause.
Options: Termination, Confidentiality, Indemnity, Arbitration, Governing Law, Force Majeure, Payment, Liability, General.

Clause: {clause}

Return valid JSON format: {{"type": "CATEGORY_NAME"}}
""",
    )
    return llm, prompt


def _fallback_classify(clause: str) -> str:
    text = clause.lower()
    for category, keywords in CLAUSE_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return json.dumps({"type": category})
    return json.dumps({"type": "General"})


def classify_clause(clause: str) -> str:
    llm, prompt = _get_llm()
    if llm is None or prompt is None:
        return _fallback_classify(clause)
    response = llm.invoke(prompt.format(clause=clause[:2000]))
    return response.content
