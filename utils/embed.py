import os
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from config import VECTOR_DIR

os.makedirs(VECTOR_DIR, exist_ok=True)

INDEX_PATH = os.path.join(VECTOR_DIR, "index.faiss")
META_PATH = os.path.join(VECTOR_DIR, "meta.pkl")

MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def embed_text(texts):
    vectors = model.encode(texts, convert_to_numpy=True)
    return vectors.astype(np.float32)


def build_index(vectors, metadata):
    faiss.normalize_L2(vectors)

    dim = vectors.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(vectors)

    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "wb") as f:
        pickle.dump(metadata, f)

    print("[embed] FAISS index saved.")


def save_embeddings_for_docs(docs):
    texts = [d["text"] for d in docs]
    metas = [{"id": d["id"], "text": d["text"]} for d in docs]

    print("[embed] Embedding", len(texts), "chunks...")
    vectors = embed_text(texts)

    build_index(vectors, metas)


def load_index():
    if not os.path.exists(INDEX_PATH):
        return None, None

    index = faiss.read_index(INDEX_PATH)
    with open(META_PATH, "rb") as f:
        meta = pickle.load(f)

    return index, meta
