"""
core/sampling.py
================
This module implements Sampling & Generation Control functions for NextGenLingo.

Controls included:
- Temperature: Adjust randomness / creativity.
- Top-K: Limit to top K most likely next tokens.
- Top-P: Nucleus sampling — consider smallest set of tokens with cumulative probability >= p.

These functions can be called directly, or integrated within prompt workflows.
"""

import os
import requests
from dotenv import load_dotenv

# Load API Key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini API base URL
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"


# ------------------------
# Common Gemini API Caller
# ------------------------
def call_gemini_with_config(prompt, generation_config):
    """
    Calls the Gemini API with a given prompt and specified generation config.
    """
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }

    data = {
        "generationConfig": generation_config,
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(GEMINI_URL, headers=headers, json=data)
    response_json = response.json()

    if response.status_code != 200:
        raise Exception(f"API call failed: {response_json}")

    return response_json["candidates"][0]["content"]["parts"][0]["text"]


# ------------------------
# Temperature Control
# ------------------------
def generate_with_temperature(prompt, temperature=1.0):
    """
    Lower temperature (e.g., 0.2) => deterministic, focused.
    Higher temperature (e.g., 0.8) => creative, varied.
    """
    return call_gemini_with_config(
        prompt,
        generation_config={"temperature": temperature}
    )


# ------------------------
# Top-K Sampling
# ------------------------
def generate_with_top_k(prompt, top_k=40):
    """
    Limits the model to consider only the top_k most likely tokens.
    Smaller K => more focused output.
    Larger K => more diverse output.
    """
    return call_gemini_with_config(
        prompt,
        generation_config={"topK": top_k}
    )


# ------------------------
# Top-P (Nucleus) Sampling
# ------------------------
def generate_with_top_p(prompt, top_p=0.9):
    """
    Considers the smallest set of tokens accounting for probability >= top_p.
    Lower top_p => more deterministic.
    Higher top_p => more creativity & variety.
    """
    return call_gemini_with_config(
        prompt,
        generation_config={"topP": top_p}
    )


# ------------------------
# Demo runs for Assignment / Project
# ------------------------
if __name__ == "__main__":
    test_prompt_temp = "Write a creative sentence about a sunset."
    print("\n--- TEMPERATURE CONTROL ---")
    print("Temperature 0.2:\n", generate_with_temperature(test_prompt_temp, 0.2))
    print("\nTemperature 0.8:\n", generate_with_temperature(test_prompt_temp, 0.8))

    test_prompt_topk = "Describe a futuristic city skyline."
    print("\n--- TOP-K CONTROL ---")
    print("Top-K 10:\n", generate_with_top_k(test_prompt_topk, 10))
    print("\nTop-K 80:\n", generate_with_top_k(test_prompt_topk, 80))

    test_prompt_topp = "Describe a mysterious island at sunset."
    print("\n--- TOP-P CONTROL ---")
    print("Top-P 0.3:\n", generate_with_top_p(test_prompt_topp, 0.3))
    print("\nTop-P 0.9:\n", generate_with_top_p(test_prompt_topp, 0.9))
