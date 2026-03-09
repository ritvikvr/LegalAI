import hashlib
import os
from functools import lru_cache

import numpy as np

try:
    from sentence_transformers import SentenceTransformer
except Exception:
    SentenceTransformer = None


@lru_cache(maxsize=1)
def _get_model():
    if os.getenv("LEGALAI_USE_ST_MODEL", "0").lower() not in {"1", "true", "yes"}:
        return None
    if SentenceTransformer is None:
        return None
    try:
        model_name = os.getenv("LEGALAI_ST_MODEL", "nlpaueb/legal-bert-base-uncased")
        return SentenceTransformer(model_name)
    except Exception:
        return None


def _hash_embedding(text: str, dim: int = 384) -> np.ndarray:
    seed = int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:16], 16)
    rng = np.random.default_rng(seed)
    vec = rng.standard_normal(dim).astype("float32")
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    return vec


def embed(texts):
    model = _get_model()
    if model is None:
        return np.array([_hash_embedding(text) for text in texts], dtype="float32")
    return model.encode(texts, show_progress_bar=False)
