import os
import requests
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_with_temperature(prompt, temperature=1.0):
    """
    Generate content from Gemini API while controlling temperature.
    Lower temp -> more deterministic.
    Higher temp -> more creative/random.
    """
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }

    # ✅ Temperature must be inside generationConfig
    data = {
        "generationConfig": {
            "temperature": temperature
        },
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    # Send POST request to Gemini API
    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()

    if response.status_code != 200:
        raise Exception(f"API call failed: {response_json}")

    # Extract only the generated text
    return response_json["candidates"][0]["content"]["parts"][0]["text"]

if __name__ == "__main__":
    test_prompt = "Write a creative sentence about a sunset."
    print("Temperature 0.2:\n", generate_with_temperature(test_prompt, 0.2))
    print("\nTemperature 0.8:\n", generate_with_temperature(test_prompt, 0.8))
