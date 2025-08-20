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
from dynamic_prompting import build_dynamic_prompt



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
    # Step 1: Embed the user query
    query_emb = embeddings.generate_embedding(user_query)
    
    # Step 2: Retrieve similar document chunks from vector store
    results = vector_store.search_similar(query_emb, top_k=top_k)
    
    # Step 3: Build retrieved context text from search results
    retrieved_context = build_context_from_results(results)
    
    # Step 4: Use provided conversation history or empty list
    conversation = conversation_history if conversation_history else []
    
    # Step 5: Build prompt dynamically using mode/intent
    prompt_text = build_dynamic_prompt(
        user_query=user_query,
        conversation_history=conversation,
        retrieved_context=retrieved_context,
        output_format=output_format,
        mode=intent
    )
    
    # Step 6: Compose system prompt and send full prompt to your LLM interface
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
