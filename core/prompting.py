import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Make sure your .env has GEMINI_API_KEY

def zero_shot_prompt_gemini(user_question):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": user_question
                    }
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()

    if response.status_code != 200:
        raise Exception(f"API call failed: {response_json}")

    # ✅ Extract just the model's generated text
    answer = response_json["candidates"][0]["content"]["parts"][0]["text"]
    return answer


if __name__ == "__main__":
    question = "Translate 'Good morning' into Spanish"
    print("Question:", question)
    print("Answer:", zero_shot_prompt_gemini(question))
