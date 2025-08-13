import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def system_user_prompt_gemini(system_prompt, user_prompt):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }

    combined_prompt = (
    "System instructions: You are NextGenLingo, an intelligent AI assistant designed to provide "
    "accurate, well-structured, and cited answers. Always respond formally, with precise explanations. "
    "When answering, mention sources if available, and respond concisely but fully. Keep tone professional and helpful.\n"
    f"User query: {user_prompt}"
)

    data = {
        "contents": [
            {
                "parts": [
                    {"text": combined_prompt}
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()

    if response.status_code != 200:
        raise Exception(f"API error: {response_json}")

    return response_json["candidates"][0]["content"]["parts"][0]["text"]



if __name__ == "__main__":
    system_text = (
        "You are NextGenLingo, an intelligent AI assistant designed to provide accurate, "
        "well-structured, and cited answers. Always respond formally, with precise explanations. "
        "Mention sources if available. Keep tone professional and helpful."
    )
    user_text = "what is Oops?"
    print("System Prompt:", system_text)
    print("User Prompt:", user_text)
    print("AI Response:", system_user_prompt_gemini(system_text, user_text))
