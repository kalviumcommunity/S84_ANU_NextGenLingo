"""
core/vector_store.py
====================
Local FAISS vector store integration for NextGenLingo.
Auto-detects embedding dimensions to avoid FAISS mismatches.
"""

import os
import json
import faiss
import numpy as np

VECTOR_STORE_INDEX_FILE = "vector_store.index"
VECTOR_STORE_META_FILE = "vector_store_meta.json"

index = None
metadata = []
EMBEDDING_DIM = None  # Will be set dynamically


def init_index(dimension: int):
    """Initializes the FAISS index with the given dimension."""
    global index, EMBEDDING_DIM
    EMBEDDING_DIM = dimension
    index = faiss.IndexFlatL2(dimension)


def load_vector_store():
    global index, metadata, EMBEDDING_DIM
    if os.path.exists(VECTOR_STORE_INDEX_FILE):
        index = faiss.read_index(VECTOR_STORE_INDEX_FILE)
        EMBEDDING_DIM = index.d
    if os.path.exists(VECTOR_STORE_META_FILE):
        try:
            with open(VECTOR_STORE_META_FILE, "r", encoding="utf-8") as f:
                metadata = json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {VECTOR_STORE_META_FILE} is empty or corrupted, resetting metadata.")
            metadata = []
            # Optionally remove the file
            os.remove(VECTOR_STORE_META_FILE)



def save_vector_store():
    """Saves FAISS index and metadata to disk."""
    faiss.write_index(index, VECTOR_STORE_INDEX_FILE)
    with open(VECTOR_STORE_META_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)


def add_document_embedding(embedding_vector, metadata_item):
    """
    Adds a new document embedding and its metadata to the store.
    Automatically initializes index if needed.
    """
    global index, metadata, EMBEDDING_DIM

    vec_np = np.array([embedding_vector], dtype='float32')

    # Auto-init index if empty
    if index is None:
        init_index(vec_np.shape[1])
    elif vec_np.shape[1] != EMBEDDING_DIM:
        raise ValueError(f"Embedding dimension {vec_np.shape[1]} "
                         f"does not match index dimension {EMBEDDING_DIM}.")

    index.add(vec_np)
    metadata.append(metadata_item)
    save_vector_store()


def search_similar(embedding_vector, top_k=3):
    """Search for top_k closest items to the given embedding."""
    if index is None or index.ntotal == 0:
        return []

    query_np = np.array([embedding_vector], dtype='float32')
    distances, indices = index.search(query_np, top_k)

    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx != -1 and idx < len(metadata):
            results.append({
                "metadata": metadata[idx],
                "distance": float(dist)
            })
    return results


# Load store at import
load_vector_store()
