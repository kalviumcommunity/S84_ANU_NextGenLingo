"""
core/embeddings.py
Embedding generation using Gemini API for NextGenLingo
"""

import os
import requests
from dotenv import load_dotenv

# Load API Key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

EMBED_URL = "https://generativelanguage.googleapis.com/v1beta/models/embedding-001:embedText"

def generate_embedding(text: str):
    """
    Generates embedding for a given text using Gemini embedding API.
    Returns a list of floats.
    """
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }
    data = {
        "text": text
    }

    response = requests.post(EMBED_URL, headers=headers, json=data)
    result = response.json()

    if response.status_code != 200:
        raise Exception(f"Embedding API call failed: {result}")
    
    # Gemini returns embeddings in:
    # { "embedding": { "value": [floats...] } }
    return result["embedding"]["value"]

if __name__ == "__main__":
    sample = "What is artificial intelligence?"
    emb = generate_embedding(sample)
    print(f"Embedding length: {len(emb)}")
    print(f"First 10 values: {emb[:10]}")
