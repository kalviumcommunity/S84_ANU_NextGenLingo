import os
import requests
from dotenv import load_dotenv

# Load Gemini API key securely from environment
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def call_gemini_api(prompt_text, generation_config=None):
    """
    Core Gemini API call helper.
    - prompt_text: str, the combined prompt text (system + examples + user question)
    - generation_config: dict, optional parameters like temperature, topK, topP
    Returns the generated text response.
    """
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }

    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt_text}
                ]
            }
        ]
    }

    if generation_config:
        data["generationConfig"] = generation_config

    response = requests.post(GEMINI_URL, headers=headers, json=data)
    response_json = response.json()

    if response.status_code != 200:
        raise Exception(f"Gemini API call failed: {response_json}")

    return response_json["candidates"][0]["content"]["parts"][0]["text"]


def zero_shot_prompt(user_question):
    """
    Zero-shot prompting: Send only the user question.
    """
    return call_gemini_api(user_question)


def one_shot_prompt(user_question):
    """
    One-shot prompting: Provide 1 example Q&A before actual user question.
    """
    example_q = "What is the capital of Germany?"
    example_a = "The capital of Germany is Berlin."

    prompt = f"Q: {example_q}\nA: {example_a}\nQ: {user_question}\nA:"
    return call_gemini_api(prompt)


def multi_shot_prompt(user_question):
    """
    Multi-shot prompting: Provide multiple Q&A examples before the user question.
    """
    examples = [
        ("What is the capital of Germany?", "The capital of Germany is Berlin."),
        ("What is the capital of Italy?", "The capital of Italy is Rome."),
        ("What is the capital of Spain?", "The capital of Spain is Madrid."),
    ]

    prompt = ""
    for q, a in examples:
        prompt += f"Q: {q}\nA: {a}\n"
    prompt += f"Q: {user_question}\nA:"
    return call_gemini_api(prompt)


def system_user_prompt(system_prompt, user_prompt, generation_config=None):
    """
    Combined system and user prompt:
    - system_prompt: Instructions defining AI assistant's behavior and style.
    - user_prompt: The actual user question or command.
    Optional generation_config for sampling controls.
    """
    combined = f"System instructions: {system_prompt}\nUser query: {user_prompt}"
    return call_gemini_api(combined, generation_config=generation_config)


if __name__ == "__main__":
    # Demo runs aligned with Project Use Cases and Architecture

    # ZERO-SHOT: Test straightforward factual QA
    q_zero = "What is the capital of France?"
    print("\n--- ZERO-SHOT PROMPT ---")
    print(f"Q: {q_zero}")
    print("A:", zero_shot_prompt(q_zero))

    # ONE-SHOT: Show guided example usage for tutoring style
    q_one = "What is the capital of Japan?"
    print("\n--- ONE-SHOT PROMPT ---")
    print(f"Q: {q_one}")
    print("A:", one_shot_prompt(q_one))

    # MULTI-SHOT: Provide multi-example input for consistent QA style
    q_multi = "What is the capital of Canada?"
    print("\n--- MULTI-SHOT PROMPT ---")
    print(f"Q: {q_multi}")
    print("A:", multi_shot_prompt(q_multi))

    # SYSTEM+USER PROMPTING: Persona-driven response with formal, detailed tone (tutoring and doc answering style)
    sys_text = (
        "You are NextGenLingo, an intelligent AI assistant specialized in "
        "providing accurate, well-structured, and cited answers. "
        "Always respond formally, include relevant examples, and cite sources when known. "
        "Be professional, concise, and helpful."
        "Answer the user's question precisely and return the response strictly formatted as JSON with the fields: "
        "'answer', 'sources' (if any). Do not include any other text."   
        
    )
    user_text = "what is python ?"

    print("\n--- SYSTEM + USER PROMPT ---")
    print("System Prompt:", sys_text)
    print("User Prompt:", user_text)
    # Example generation config: default or supply e.g. temperature=0.7 for creativity control
    print("A:", system_user_prompt(sys_text, user_text))
