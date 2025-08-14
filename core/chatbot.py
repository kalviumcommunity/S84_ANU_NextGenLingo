"""
core/chatbot.py
================
NextGenLingo AI Assistant with:
- Persistent Multi-turn Contextual Memory
- Dynamic Prompting
- Chain-of-Thought Prompting (prefix: cot:)
- Ready for RAG integration (retrieved context placeholder)
"""

import os
import re
import sys
import json
from dotenv import load_dotenv

# Ensure project root is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core import prompting, function_calling, dynamic_prompting, chain_of_thought
# RAG Engine will be integrated later
# from core import rag_engine

load_dotenv()

MEMORY_FILE = "conversation_memory.json"

# -----------------------
# Persistent Memory Helpers
# -----------------------
def load_conversation_history():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_conversation_history(history):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

conversation_history = load_conversation_history()

# -----------------------
# Intent Detection
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
# Main Chat Loop
# -----------------------
def run_chatbot():
    print("\n🤖 NextGenLingo AI Assistant (Dynamic + CoT Ready)")
    print("Type 'exit' to quit.\n")
    print("💡 Commands: \n"
          "   cot: <question>       → Hidden Chain-of-Thought (final answer only)\n"
          "   cot: reason <question> → Chain-of-Thought with reasoning steps\n"
          "   doc: <question>        → Use RAG-based retrieval (coming next)\n"
    )

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye! 👋")
            break

        # 1. Check automation intents
        intent, params = detect_intent(user_input)
        if intent:
            print(f"[Intent] Detected action: {intent}")
            result = function_calling.execute_action(intent, params)
            print("Assistant:", result)
            conversation_history.append({"user": user_input, "assistant": result})
            save_conversation_history(conversation_history)
            continue

        # 2. Chain-of-Thought mode
        if user_input.startswith("cot:"):
            cot_query = user_input.replace("cot:", "").strip()
            show_reasoning = False
            if cot_query.startswith("reason "):
                cot_query = cot_query.replace("reason ", "").strip()
                show_reasoning = True
            ai_response = chain_of_thought.chain_of_thought_prompt(cot_query, show_reasoning)
            print("Assistant:", ai_response)
            conversation_history.append({"user": user_input, "assistant": ai_response})
            save_conversation_history(conversation_history)
            continue

        # 3. RAG doc-query (placeholder until rag_engine.py done)
        if user_input.startswith("doc:"):
            doc_query = user_input.replace("doc:", "").strip()
            # This will use RAG engine after we implement it
            # ai_response = rag_engine.query_with_rag(doc_query)
            ai_response = "[RAG placeholder] Retrieved context answer will go here."
            print("Assistant:", ai_response)
            conversation_history.append({"user": user_input, "assistant": ai_response})
            save_conversation_history(conversation_history)
            continue

        # 4. Dynamic Prompting (default mode)
        # Placeholder for RAG retrieved context until rag_engine is ready
        retrieved_context = None
        # retrieved_context = rag_engine.get_context(user_input)  # Once implemented

        dynamic_prompt = dynamic_prompting.build_dynamic_prompt(
            user_query=user_input,
            conversation_history=conversation_history,
            retrieved_context=retrieved_context,
            output_format=None  # Could be "Markdown" or "JSON"
        )
        ai_response = prompting.system_user_prompt(
            "You are NextGenLingo, a helpful and context-aware assistant.",
            dynamic_prompt
        )

        print("Assistant:", ai_response)

        # Save to persistent memory
        conversation_history.append({"user": user_input, "assistant": ai_response})
        save_conversation_history(conversation_history)

# -----------------------
if __name__ == "__main__":
    run_chatbot()
