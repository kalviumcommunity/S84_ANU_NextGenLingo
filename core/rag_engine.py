"""
core/rag_engine.py
==================
Retrieval Augmented Generation (RAG) orchestration for NextGenLingo.
"""

import embeddings
import vector_store
import prompting
from dynamic_prompting import (
    build_summary_prompt,
    build_quiz_prompt,
    build_flashcards_prompt,
    build_code_review_prompt,
    build_debate_prompt,
)


def add_document(text, doc_id=None, source=None):
    """
    Add a new document text chunk to the vector store with embedding and metadata.
    """
    emb = embeddings.generate_embedding(text)
    meta = {"id": doc_id, "source": source, "content": text}
    vector_store.add_document_embedding(emb, meta)


def build_context_from_results(results):
    """Format retrieved search results into a context block for prompting."""
    context_parts = []
    for res in results:
        meta = res.get("metadata", {})
        source_name = meta.get("source", "unknown source")
        snippet = meta.get("content", "")
        context_parts.append(f"[Source: {source_name}]\n{snippet}\n")
    return "\n---\n".join(context_parts)


def query_with_rag(user_query, conversation_history=None, top_k=3, output_format=None, intent="summary"):
    """
    Runs a query through the RAG pipeline:
    1. Embed query
    2. Search vector DB
    3. Build context
    4. Construct dynamic prompt based on intent/mode
    5. Get answer from LLM

    Supports optional output_format (e.g., "json", "markdown") for structured responses.
    """
    # Step 1: Embed query
    query_emb = embeddings.generate_embedding(user_query)

    # Step 2: Retrieve similar docs
    results = vector_store.search_similar(query_emb, top_k=top_k)

    # Step 3: Context from retrieved docs
    retrieved_context = build_context_from_results(results)

    # Step 4: Append conversation history if provided
    conversation = conversation_history if conversation_history else []

    # Step 5: Build prompt with mode/intent
    if intent == "summary":
        prompt_text = build_summary_prompt(user_query, conversation, retrieved_context, output_format)
    elif intent == "quiz":
        prompt_text = build_quiz_prompt(user_query, conversation, retrieved_context)
    elif intent == "flashcards":
        prompt_text = build_flashcards_prompt(user_query, conversation, retrieved_context)
    elif intent == "code_review":
        prompt_text = build_code_review_prompt(user_query, conversation, retrieved_context)
    elif intent == "debate":
        prompt_text = build_debate_prompt(user_query, conversation, retrieved_context)
    else:
        # Default fallback to summary prompt
        prompt_text = build_summary_prompt(user_query, conversation, retrieved_context, output_format)

    # Step 6: Send to LLM
    system_prompt = (
        "You are NextGenLingo, an intelligent AI assistant. "
        "Use the provided context to answer the user accurately with citations."
    )
    answer = prompting.system_user_prompt(system_prompt, prompt_text)
    return answer


if __name__ == "__main__":
    # TEMP: clear existing store for clean test
    import os
    for f in ["vector_store.index", "vector_store_meta.json"]:
        if os.path.exists(f):
            os.remove(f)
    # Add a sample doc
    sample_doc = "Paris is the capital city of France, known for the Eiffel Tower."
    add_document(sample_doc, doc_id="doc1", source="SampleDoc.txt")

    # Run a query as a test
    query = "What is the capital of France?"
    print("RAG Answer:\n", query_with_rag(query))
