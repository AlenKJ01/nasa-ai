import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from utils.embed import load_index, MODEL_NAME
from config import TOP_K

model = SentenceTransformer(MODEL_NAME)


def query_embedding(text):
    vec = model.encode([text], convert_to_numpy=True)[0]
    vec = vec.astype(np.float32)
    return vec


def retrieve(query, top_k=TOP_K):
    index, metas = load_index()
    if index is None:
        raise RuntimeError("Index not built. Run /init_index first.")

    qvec = query_embedding(query)
    qvec = qvec.reshape(1, -1)
    faiss.normalize_L2(qvec)

    D, I = index.search(qvec, top_k)

    return [metas[i] for i in I[0] if i < len(metas)]
