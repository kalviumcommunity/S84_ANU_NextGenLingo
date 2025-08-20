import prompting

def build_summary_prompt(user_query, conversation_history=None, retrieved_context=None, output_format=None):
    system_instructions = (
        "You are NextGenLingo, an advanced AI assistant. "
        "Provide a concise summary of the provided document or content in maximum 2 lines. "
        "Use the retrieved context fully to ground your summary."
    )
    
    prompt_parts = [f"System: {system_instructions}"]

    if conversation_history:
        history_str = ""
        for turn in conversation_history:
            history_str += f"User: {turn['user']}\nAssistant: {turn['assistant']}\n"
        prompt_parts.append(f"Conversation History:\n{history_str.strip()}")

    if retrieved_context:
        prompt_parts.append(f"Document Content:\n{retrieved_context}")

    prompt_parts.append(f"User: {user_query}")

    if output_format:
        prompt_parts.append(f"Please respond in {output_format} format.")

    return "\n\n".join(prompt_parts)

# dynamic_prompting.py
"""
Dynamic prompt construction for NextGenLingo.
Includes dedicated prompt templates for multiple chatbot modes.
"""

def build_summary_prompt(user_query, conversation_history=None, retrieved_context=None, output_format=None):
    system_instructions = (
        "You are NextGenLingo, an advanced AI assistant. "
        "Provide a concise summary of the provided document or content in maximum 2 lines. "
        "Use the retrieved context fully to ground your summary."
    )

    prompt_parts = [f"System: {system_instructions}"]

    if conversation_history:
        history_str = ""
        for turn in conversation_history:
            history_str += f"User: {turn['user']}\nAssistant: {turn['assistant']}\n"
        prompt_parts.append(f"Conversation History:\n{history_str.strip()}")

    if retrieved_context:
        prompt_parts.append(f"Document Content:\n{retrieved_context}")

    prompt_parts.append(f"User: {user_query}")

    if output_format:
        prompt_parts.append(f"Please respond in {output_format} format.")

    return "\n\n".join(prompt_parts)


def build_quiz_prompt(user_query, conversation_history=None, retrieved_context=None):
    system_instructions = (
        "You are NextGenLingo. "
        "Based on the provided document content, create 3 multiple-choice questions "
        "with exactly 4 options each and indicate the correct option clearly as 'Correct: X' where X is A/B/C/D. "
        "Each question must be in this format:\n"
        "1. <question here>\n"
        "A. <option A>\n"
        "B. <option B>\n"
        "C. <option C>\n"
        "D. <option D>\n"
        "Correct: <A/B/C/D>\n"
        "Repeat for 3 questions and do NOT add explanations or other text."
    )
    
    prompt_parts = [f"System: {system_instructions}"]

    if conversation_history:
        history_str = ""
        for turn in conversation_history:
            history_str += f"User: {turn['user']}\nAssistant: {turn['assistant']}\n"
        prompt_parts.append(f"Conversation History:\n{history_str.strip()}")

    if retrieved_context:
        prompt_parts.append(f"Document Content:\n{retrieved_context}")

    prompt_parts.append(f"User: {user_query}")
    return "\n\n".join(prompt_parts)



def build_flashcards_prompt(user_query, conversation_history=None, retrieved_context=None):
    system_instructions = (
        "You are NextGenLingo. Create concise flashcards (question and answer pairs) "
        "based on the provided content to help a user memorize key concepts."
    )

    prompt_parts = [f"System: {system_instructions}"]

    if conversation_history:
        history_str = ""
        for turn in conversation_history:
            history_str += f"User: {turn['user']}\nAssistant: {turn['assistant']}\n"
        prompt_parts.append(f"Conversation History:\n{history_str.strip()}")

    if retrieved_context:
        prompt_parts.append(f"Document Content:\n{retrieved_context}")

    prompt_parts.append(f"User: {user_query}")
    prompt_parts.append("Please format the answer as flashcard pairs.")

    return "\n\n".join(prompt_parts)


def build_code_review_prompt(user_query, conversation_history=None, retrieved_context=None):
    system_instructions = (
        "You are NextGenLingo, specializing in code analysis. "
        "Review the provided code or technical content and provide clear explanations, "
        "suggest improvements, and point out issues."
    )

    prompt_parts = [f"System: {system_instructions}"]

    if conversation_history:
        history_str = ""
        for turn in conversation_history:
            history_str += f"User: {turn['user']}\nAssistant: {turn['assistant']}\n"
        prompt_parts.append(f"Conversation History:\n{history_str.strip()}")

    if retrieved_context:
        prompt_parts.append(f"Code or technical content:\n{retrieved_context}")

    prompt_parts.append(f"User: {user_query}")

    return "\n\n".join(prompt_parts)


def build_debate_prompt(user_query, conversation_history=None, retrieved_context=None):
    system_instructions = (
        "You are NextGenLingo. Engage in a debate format with the user on the provided topic. "
        "Provide arguments supporting and opposing the topic based on the context."
    )

    prompt_parts = [f"System: {system_instructions}"]

    if conversation_history:
        history_str = ""
        for turn in conversation_history:
            history_str += f"User: {turn['user']}\nAssistant: {turn['assistant']}\n"
        prompt_parts.append(f"Conversation History:\n{history_str.strip()}")

    if retrieved_context:
        prompt_parts.append(f"Debate topic context:\n{retrieved_context}")

    prompt_parts.append(f"User: {user_query}")

    return "\n\n".join(prompt_parts)



def build_dynamic_prompt(user_query, conversation_history=None, retrieved_context=None, output_format=None, mode="summary"):
    """
    Master prompt builder selecting prompt template based on mode.
    """
    if mode == "summary":
        return build_summary_prompt(user_query, conversation_history, retrieved_context, output_format)
    elif mode == "quiz":
        return build_quiz_prompt(user_query, conversation_history, retrieved_context)
    elif mode == "flashcards":
        return build_flashcards_prompt(user_query, conversation_history, retrieved_context)
    elif mode == "code_review":
        return build_code_review_prompt(user_query, conversation_history, retrieved_context)
    elif mode == "debate":
        return build_debate_prompt(user_query, conversation_history, retrieved_context)
    else:
        # default fallback
        return build_summary_prompt(user_query, conversation_history, retrieved_context, output_format)


