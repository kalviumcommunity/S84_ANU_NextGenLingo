"""
core/similarity.py
==================
Similarity calculations for NextGenLingo RAG:
- Cosine Similarity
- Euclidean (L2) Distance

Uses Gemini API to embed texts and compares embeddings.
"""

import numpy as np
from embeddings import generate_embedding  # Adjust import based on your project structure


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


def l2_distance(vec_a, vec_b):
    """
    Calculate Euclidean (L2) distance between two vectors.
    Lower distance means higher similarity.
    """
    a = np.array(vec_a)
    b = np.array(vec_b)
    return np.linalg.norm(a - b)


if __name__ == "__main__":
    # Sample texts
    query = "What is the capital of France?"
    doc_text = "Paris is the capital city of France. It is known for the Eiffel Tower."
    unrelated_text = "Bananas are a yellow fruit commonly eaten for breakfast."

    # Generate embeddings using your Gemini embedding pipeline
    emb_query = generate_embedding(query)
    emb_doc = generate_embedding(doc_text)
    emb_unrelated = generate_embedding(unrelated_text)

    # Compute cosine similarities
    cosine_sim_related = cosine_similarity(emb_query, emb_doc)
    cosine_sim_unrelated = cosine_similarity(emb_query, emb_unrelated)
    print(f"Cosine Similarity (query vs. related doc): {cosine_sim_related:.4f}")
    print(f"Cosine Similarity (query vs. unrelated doc): {cosine_sim_unrelated:.4f}")

    # Compute Euclidean distances
    l2_dist_related = l2_distance(emb_query, emb_doc)
    l2_dist_unrelated = l2_distance(emb_query, emb_unrelated)
    print(f"L2 Distance (query vs. related doc): {l2_dist_related:.2f}")
    print(f"L2 Distance (query vs. unrelated doc): {l2_dist_unrelated:.2f}")
