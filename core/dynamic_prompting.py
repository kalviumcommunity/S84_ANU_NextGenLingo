"""
core/dynamic_prompting.py
=========================
Dynamic prompt construction for NextGenLingo.
Builds prompts at runtime using memory, retrieved docs, and system instructions.
"""

import prompting

def build_dynamic_prompt(user_query, conversation_history=None, retrieved_context=None, output_format=None):
    """
    Creates a dynamic prompt string from multiple components.
    :param user_query: str - Current user question or command.
    :param conversation_history: list of dicts [{'user': '', 'assistant': ''}, ...]
    :param retrieved_context: str - Extra context from RAG or other tools.
    :param output_format: str - Desired output format (JSON, Markdown, etc.)
    :return: Constructed final prompt string.
    """
    prompt_parts = []

    # 1. System persona
    system_instructions = (
        "You are NextGenLingo, an advanced conversational AI. "
        "Always provide accurate, well-structured, and concise answers. "
        "Cite sources if relevant."
    )
    prompt_parts.append(f"System: {system_instructions}")

    # 2. Conversation history
    if conversation_history:
        history_str = ""
        for turn in conversation_history:
            history_str += f"User: {turn['user']}\nAssistant: {turn['assistant']}\n"
        prompt_parts.append(f"Conversation History:\n{history_str.strip()}")

    # 3. Retrieved context (if using RAG)
    if retrieved_context:
        prompt_parts.append(f"Additional Context:\n{retrieved_context}")

    # 4. Output formatting
    if output_format:
        prompt_parts.append(f"Please respond in {output_format} format.")

    # 5. The new user query
    prompt_parts.append(f"User: {user_query}")

    # Combine into single string
    final_prompt = "\n\n".join(prompt_parts)
    return final_prompt

# Simple test run
if __name__ == "__main__":
    history = [
        {"user": "What's the capital of Germany?", "assistant": "Berlin."}
    ]
    context = "Germany is located in Central Europe. Berlin is its largest city."
    query = "What is the population of the capital?"
    dynamic_prompt = build_dynamic_prompt(query, history, context, output_format="Markdown")
    print("\n--- DYNAMIC PROMPT ---")
    print(dynamic_prompt)

    # Send to Gemini
    print("\n--- AI RESPONSE ---")
    print(prompting.zero_shot_prompt(dynamic_prompt))
