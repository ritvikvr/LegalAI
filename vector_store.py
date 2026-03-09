import faiss
import numpy as np

index = None
documents = []


def _ensure_2d_array(values) -> np.ndarray:
    arr = np.asarray(values, dtype="float32")
    if arr.ndim == 1:
        arr = arr.reshape(1, -1)
    if arr.ndim != 2:
        raise ValueError("Embeddings must be a 2D array")
    return arr


def add_embeddings(embeddings, chunks):
    global index
    arr = _ensure_2d_array(embeddings)

    if len(chunks) != arr.shape[0]:
        raise ValueError("Each embedding must map to one chunk")

    if index is None:
        index = faiss.IndexFlatL2(arr.shape[1])
    elif index.d != arr.shape[1]:
        raise ValueError(f"Embedding dimension mismatch: expected {index.d}, got {arr.shape[1]}")

    index.add(arr)
    documents.extend(chunks)


def semantic_search(query_embedding, k=5):
    if index is None or not documents:
        return []

    query = _ensure_2d_array(query_embedding)
    if query.shape[1] != index.d:
        raise ValueError(f"Query embedding dimension mismatch: expected {index.d}, got {query.shape[1]}")

    top_k = min(k, len(documents))
    _, idx = index.search(query, top_k)
    return [documents[i] for i in idx[0] if i >= 0]
