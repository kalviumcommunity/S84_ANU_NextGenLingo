import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def one_shot_prompt_gemini(user_question):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }

    # Example Q&A to guide the model (this is the 'one-shot')
    example_input = "What is the capital of Germany?"
    example_answer = "The capital of Germany is Berlin."

    # Structure: first example, then actual question
    data = {
        "contents": [
            {
                "parts": [
                    {"text": f"Q: {example_input}\nA: {example_answer}\nQ: {user_question}\nA:"}
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()

    if response.status_code != 200:
        raise Exception(f"API call failed: {response_json}")

    # Extract clean text
    answer = response_json["candidates"][0]["content"]["parts"][0]["text"]
    return answer

if __name__ == "__main__":
    question = "What is the capital of Japan?"
    print("Question:", question)
    print("Answer:", one_shot_prompt_gemini(question))
