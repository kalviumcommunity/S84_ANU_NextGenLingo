"""
core/chatbot.py
================
Main chatbot orchestrator for NextGenLingo.

Flow:
1. Get user input from the console
2. Detect if this is an automation task or a general query
3. If automation → call backend functions (function_calling.py)
4. Else → forward to LLM via prompting functions (prompting.py)
5. Display response
"""

import os
import re
import sys
from datetime import datetime
from dotenv import load_dotenv

# Ensure project root is in sys.path so imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core import prompting
from core import function_calling

# Load environment variables (Gemini API key, etc.)
load_dotenv()

# -----------------------
# Simple Rule-based Intent Detection
# -----------------------
def detect_intent(user_input: str):
    """
    Basic keyword-based intent detection.
    Returns:
        (intent_name, params_dict)
    """
    text = user_input.lower()

    # Email intent
    if "send email" in text:
        match_to = re.search(r"to ([\w\.-]+@[\w\.-]+)", user_input)
        to_email = match_to.group(1) if match_to else "unknown@example.com"
        subject = "No Subject"
        body = user_input
        return "send_email", {"to": to_email, "subject": subject, "body": body}

    # To-do list intent
    elif "add task" in text or "todo" in text:
        return "add_todo", {"task": user_input.replace("add task", "").strip()}

    # Weather intent
    elif "weather" in text:
        location_match = re.search(r"in ([A-Za-z ]+)", user_input)
        location = location_match.group(1) if location_match else "your area"
        return "weather", {"location": location}

    # Date/Time intent
    elif "time" in text or "date" in text:
        return "get_time", {}

    # Default → let LLM handle it
    return None, {}

# -----------------------
# Chatbot Main Loop
# -----------------------
def run_chatbot():
    print("\n🤖 NextGenLingo AI Assistant")
    print("Type 'exit' to quit.\n")

    last_response = ""  # For basic correction handling

    while True:
        user_input = input("You: ").strip()

        # Exit command
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye! 👋")
            break

        # Handle simple corrections
        if user_input.lower() in ["wrong", "no", "incorrect", "that's not right"]:
            print("Assistant: Sorry, let me correct that.")
            if "time" in last_response.lower() or "date" in last_response.lower():
                corrected = function_calling.execute_action("get_time", {})
                print(f"Assistant: {corrected}")
                last_response = corrected
                continue
            else:
                print("Assistant: Could you please clarify what needs correcting?")
                continue

        # Detect automation intent
        intent, params = detect_intent(user_input)
        if intent:
            print(f"[Intent] Detected action: {intent}")
            result = function_calling.execute_action(intent, params)
            print("Assistant:", result)
            last_response = result
            continue

        # Select prompting style
        if user_input.startswith("multi:"):
            query = user_input.replace("multi:", "").strip()
            ai_response = prompting.multi_shot_prompt(query)

        elif user_input.startswith("one:"):
            query = user_input.replace("one:", "").strip()
            ai_response = prompting.one_shot_prompt(query)

        elif user_input.startswith("sys:"):
            query = user_input.replace("sys:", "").strip()
            sys_prompt = (
                "You are NextGenLingo, an intelligent AI assistant that provides "
                "accurate, well-structured, cited answers in a formal tone."
            )
            ai_response = prompting.system_user_prompt(sys_prompt, query)

        else:
            # Default → Zero-shot
            ai_response = prompting.zero_shot_prompt(user_input)

        print("Assistant:", ai_response)
        last_response = ai_response

# -----------------------
# Entry Point
# -----------------------
if __name__ == "__main__":
    run_chatbot()
