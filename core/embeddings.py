"""
core/embeddings.py
==================
Embedding generation using Gemini API for NextGenLingo.

This module generates numerical vector representations for a given text
using the Google Gemini Embedding model `gemini-embedding-001`.

You can use these embeddings for:
- Semantic search
- Document similarity
- Retrieval Augmented Generation (RAG) pipeline
"""

import os
import requests
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Correct Gemini Embedding endpoint
GEMINI_EMBEDDING_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-embedding-001:embedContent"
)

def generate_embedding(text: str):
    """
    Generate an embedding vector for the input text using the Gemini embedding model.
    Returns a list of floats.
    """
    if not GEMINI_API_KEY:
        raise ValueError("❌ GEMINI_API_KEY not found in environment variables.")

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }

    # IMPORTANT: Use singular "content" and correct "embeddingConfig" key
    payload = {
        "model": "models/gemini-embedding-001",
        "content": {
            "parts": [
                {"text": text}
            ]
        }
        # "embeddingConfig" is optional in current API, remove if unsupported.
        # Uncomment if you need specific dimensionality:
        # ,
        # "embeddingConfig": {
        #     "outputDimensionality": 768
        # }
    }

    response = requests.post(GEMINI_EMBEDDING_URL, headers=headers, json=payload)
    response_json = response.json()

    if response.status_code != 200:
        raise Exception(f"❌ Embedding API call failed: {response_json}")

    # The embedding vector is in response_json['embedding']['values']
    embedding_data = response_json.get("embedding", {}).get("values")
    if not embedding_data:
        raise Exception(f"❌ No embedding returned: {response_json}")

    return embedding_data


if __name__ == "__main__":
    # Standalone test
    sample_text = "What is the capital of France?"
    embedding = generate_embedding(sample_text)
    print(f"✅ Embedding vector length: {len(embedding)}")
    print("🔹 First 10 values:", embedding[:10])
