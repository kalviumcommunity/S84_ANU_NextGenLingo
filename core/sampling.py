import os
import requests
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_with_top_p(prompt, top_p=0.9):
    """
    Generate content from Gemini API controlling top-p sampling.
    - Lower top_p restricts to higher probability tokens, more focused output.
    - Higher top_p allows more token variety and creativity.
    """
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }
    data = {
        "generationConfig": {
            "topP": top_p
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
    test_prompt = "Describe a mysterious island at sunset , in maximum 3 lines."
    print("Top-P 0.3:\n", generate_with_top_p(test_prompt, 0.3))
    print("\nTop-P 0.9:\n", generate_with_top_p(test_prompt, 0.9))
