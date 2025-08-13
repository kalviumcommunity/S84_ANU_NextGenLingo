"""
core/chatbot.py
================
NextGenLingo AI Assistant with Multi-turn Contextual Memory
"""

import os
import re
import sys
from dotenv import load_dotenv
import json

# Ensure project root is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core import prompting
from core import function_calling

# Load environment variables
load_dotenv()

# Conversation history list
conversation_history = []

MEMORY_FILE = "conversation_memory.json"

def load_conversation_history():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_conversation_history(history):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

# -----------------------
# Intent Detection (same as before)
# -----------------------
def detect_intent(user_input: str):
    text = user_input.lower()
    if "send email" in text:
        match_to = re.search(r"to ([\w\.-]+@[\w\.-]+)", user_input)
        return "send_email", {"to": match_to.group(1) if match_to else "unknown@example.com",
                              "subject": "No Subject",
                              "body": user_input}
    elif "add task" in text or "todo" in text:
        return "add_todo", {"task": user_input.replace("add task", "").strip()}
    elif "weather" in text:
        location_match = re.search(r"in ([A-Za-z ]+)", user_input)
        return "weather", {"location": location_match.group(1) if location_match else "your area"}
    elif "time" in text or "date" in text:
        return "get_time", {}
    return None, {}

# -----------------------
# Build Context Prompt from History
# -----------------------
def build_contextual_prompt(latest_user_input):
    context_str = ""
    for turn in conversation_history:
        context_str += f"User: {turn['user']}\nAssistant: {turn['assistant']}\n"
    context_str += f"User: {latest_user_input}\nAssistant:"
    return context_str

# -----------------------
# Main Chat Loop with Memory
# -----------------------
def run_chatbot():
    print("\n🤖 NextGenLingo AI Assistant (with Context Memory)")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye! 👋")
            break

        # Detect intents first
        intent, params = detect_intent(user_input)
        if intent:
            print(f"[Intent] Detected action: {intent}")
            result = function_calling.execute_action(intent, params)
            print("Assistant:", result)
            conversation_history.append({"user": user_input, "assistant": result})
            continue

        # Build context including history
        prompt_with_context = build_contextual_prompt(user_input)

        # Use a system instruction for the AI to behave consistently
        system_instruction = (
            "You are NextGenLingo, an intelligent AI assistant that uses the full conversation "
            "history to give accurate, coherent, and context-aware responses."
        )

        ai_response = prompting.system_user_prompt(system_instruction, prompt_with_context)

        print("Assistant:", ai_response)

        # Save to memory
        conversation_history.append({"user": user_input, "assistant": ai_response})

# -----------------------
if __name__ == "__main__":
    run_chatbot()
