import os
import requests
from dotenv import load_dotenv

# Load API Key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def generate_with_stop_sequence(prompt, stop_sequences):
    """
    Generates text with a stop sequence to cut off output when a specific string is encountered.
    
    :param prompt: The text prompt for the LLM.
    :param stop_sequences: List of strings where generation will stop.
    """
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }

    data = {
        "generationConfig": {
            "stopSequences": stop_sequences
        },
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

if __name__ == "__main__":
    prompt_text = (
        "List 3 fruits and then say END.\n"
        "Fruits:"
    )
    # The model will stop when it outputs "END"
    print(generate_with_stop_sequence(prompt_text, ["END"]))
