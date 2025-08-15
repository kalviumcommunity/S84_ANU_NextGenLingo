"""
core/similarity.py
==================
Cosine Similarity in the context of NextGenLingo RAG.
- Uses Gemini API to embed two texts,
- Computes similarity between their embeddings.
"""

import numpy as np
from embeddings import generate_embedding

def cosine_similarity(vec_a, vec_b):
    """Cosine similarity between two 1D vectors."""
    a = np.array(vec_a)
    b = np.array(vec_b)
    dot = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)

if __name__ == "__main__":
    # Real example: Compare a user query to a document chunk
    query = "What is the capital of France?"
    doc_text = "Paris is the capital city of France. It is known for the Eiffel Tower."

    # Get Gemini embeddings for both (uses your project embedding pipeline)
    emb_query = generate_embedding(query)
    emb_doc = generate_embedding(doc_text)

    # Compute cosine similarity (should be close to 1 for matching content)
    score = cosine_similarity(emb_query, emb_doc)
    print(f"Cosine Similarity (query vs. doc): {score:.4f}")

    # For unrelated texts, similarity will be near 0:
    unrelated = "Bananas are a yellow fruit commonly eaten for breakfast."
    emb_unrelated = generate_embedding(unrelated)
    unrelated_score = cosine_similarity(emb_query, emb_unrelated)
    print(f"Cosine Similarity (query vs. unrelated): {unrelated_score:.4f}")
