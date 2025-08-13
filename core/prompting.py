import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def multi_shot_prompt_gemini(user_question):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }

    # Multi-shot examples
    examples = [
        ("What is the capital of Germany?", "The capital of Germany is Berlin."),
        ("What is the capital of Italy?", "The capital of Italy is Rome."),
        ("What is the capital of Spain?", "The capital of Spain is Madrid.")
    ]

    # Build multi-shot prompt
    multi_shot_text = ""
    for q, a in examples:
        multi_shot_text += f"Q: {q}\nA: {a}\n"

    multi_shot_text += f"Q: {user_question}\nA:"

    data = {
        "contents": [
            {
                "parts": [
                    {"text": multi_shot_text}
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()

    if response.status_code != 200:
        raise Exception(f"API call failed: {response_json}")

    answer = response_json["candidates"][0]["content"]["parts"][0]["text"]
    return answer


if __name__ == "__main__":
    question = "What is the capital of INDIA?"
    print("Question:", question)
    print("Answer:", multi_shot_prompt_gemini(question))
