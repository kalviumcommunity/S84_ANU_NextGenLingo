"""
core/rag_engine.py
==================
Retrieval Augmented Generation (RAG) orchestration for NextGenLingo.
"""

import embeddings, vector_store, prompting, dynamic_prompting


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


def query_with_rag(user_query, conversation_history=None, top_k=3):
    """
    Runs a query through the RAG pipeline:
    1. Embed query
    2. Search vector DB
    3. Build context
    4. Construct dynamic prompt
    5. Get answer from LLM
    """
    # Step 1: Query embedding
    query_emb = embeddings.generate_embedding(user_query)

    # Step 2: Retrieve similar docs
    results = vector_store.search_similar(query_emb, top_k=top_k)

    # Step 3: Context from retrieved docs
    retrieved_context = build_context_from_results(results)

    # Step 4: Append conversation history if provided
    conversation = conversation_history if conversation_history else []

    # Step 5: Dynamic prompt with context
    prompt_text = dynamic_prompting.build_dynamic_prompt(
        user_query=user_query,
        conversation_history=conversation,
        retrieved_context=retrieved_context,
        output_format=None
    )

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

    # Run a query
    query = "What is the capital of France?"
    print("RAG Answer:\n", query_with_rag(query))
