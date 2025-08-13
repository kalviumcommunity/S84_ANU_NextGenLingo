import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_with_top_k(prompt, top_k=40):
    """
    Generate content from Gemini API while controlling top-k sampling.
    - Lower top_k restricts choices, resulting in more focused output.
    - Higher top_k allows more diverse output.
    """
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }

    data = {
        "generationConfig": {
            "topK": top_k
        },
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()

    if response.status_code != 200:
        raise Exception(f"API call failed: {response_json}")

    return response_json["candidates"][0]["content"]["parts"][0]["text"]

if __name__ == "__main__":
    test_prompt = "Describe a futuristic city skyline."
    print("Top-K 10:\n", generate_with_top_k(test_prompt, 10))
    print("\nTop-K 80:\n", generate_with_top_k(test_prompt, 80))
