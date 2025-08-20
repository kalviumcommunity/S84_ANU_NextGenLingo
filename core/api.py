import re
import io
import pdfplumber
from typing import List

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse

import embeddings
import vector_store
import prompting
import dynamic_prompting
from rag_engine import query_with_rag, add_document

app = FastAPI()

# Configure CORS middleware for frontend origin (adjust port if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Parse quiz output from LLM into structured JSON
def parse_quiz(llm_output):
    quiz = []
    if not llm_output.strip():
        return quiz

    q_blocks = re.split(r"\n(?=\d+\.)", llm_output)
    for qb in q_blocks:
        m = re.match(
            r"\d+\.\s*(.+?)\nA\.\s*(.+)\nB\.\s*(.+)\nC\.\s*(.+)\nD\.\s*(.+)\nCorrect:\s*([A-D])", 
            qb, re.DOTALL
        )
        if m:
            question, oA, oB, oC, oD, correct = m.groups()
            options = [oA.strip(), oB.strip(), oC.strip(), oD.strip()]
            option_labels = ['A', 'B', 'C', 'D']
            quiz.append({
                "id": f"q{len(quiz)+1}",
                "question": question.strip(),
                "options": options,
                "answer": options[option_labels.index(correct)]
            })
    return quiz

@app.post("/chat")
async def chat_endpoint(request: Request):
    print("Received chat request")
    data = await request.json()
    query = data.get("query", "")
    intent = data.get("intent", "summary")
    print("Query:", query, "Intent:", intent)

    try:
        answer = query_with_rag(query, conversation_history=None, intent=intent)
        print("RAG output:", answer)

        if intent == "quiz":
            print("Raw Quiz LLM Output:\n", answer)
            questions = parse_quiz(answer)
            print("Parsed Questions:\n", questions)
            if not questions:
                return {
                    "type": "text",
                    "response": "Sorry, could not generate a quiz. Try changing your request, or upload more relevant content.",
                    "sources": []
                }
            return {"type": "quiz", "questions": questions, "sources": []}

        # For other intents, or fallback
        return {"type": "text", "response": answer, "sources": []}

    except Exception as e:
        print("Backend error:", e)
        return {"type": "text", "response": f"Error: {str(e)}", "sources": []}



@app.post("/upload")
async def upload_endpoint(file: UploadFile = File(...)):
    filename = file.filename.lower()
    content = await file.read()
    text = ""

    if filename.endswith(".pdf"):
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            pages = [page.extract_text() or "" for page in pdf.pages]
            text = "\n".join(pages)
    elif filename.endswith(".txt"):
        text = content.decode("utf-8", errors="ignore")
    else:
        return {"error": "Unsupported file format. Please upload PDF or TXT."}

    # Chunk text and embed + index
    chunks = [text[i : i + 800] for i in range(0, len(text), 800)]

    for i, chunk in enumerate(chunks):
        embedding = embeddings.generate_embedding(chunk)
        metadata_item = {
            "text": chunk,
            "doc_id": f"{file.filename}-{i}",
            "source": file.filename,
        }
        vector_store.add_document_embedding(embedding, metadata_item)

    return {"status": "success", "chunks_added": len(chunks)}


@app.post("/upload-multi")
async def upload_multi_endpoint(files: List[UploadFile] = File(...)):
    total_chunks = 0
    for file in files:
        content = await file.read()
        text = ""
        if file.filename.lower().endswith(".pdf"):
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                pages = [page.extract_text() or "" for page in pdf.pages]
                text = "\n".join(pages)
        elif file.filename.lower().endswith(".txt"):
            text = content.decode("utf-8", errors="ignore")
        # Further formats can be added here

        chunks = [text[i : i + 800] for i in range(0, len(text), 800)]

        for i, chunk in enumerate(chunks):
            embedding = embeddings.generate_embedding(chunk)
            metadata_item = {
                "text": chunk,
                "doc_id": f"{file.filename}-{i}",
                "source": file.filename,
            }
            vector_store.add_document_embedding(embedding, metadata_item)
        total_chunks += len(chunks)

    return {"status": "success", "total_chunks_added": total_chunks}


async def your_llm_stream(query):
    # Example placeholder for your streaming LLM API call.
    # Replace with real streaming call to your LLM provider.
    async for partial in llm_api.stream_generate(query):
        yield partial


@app.get("/chat-stream")
async def chat_stream(request: Request):
    query = request.query_params.get("query", "")
    async def event_generator():
        async for chunk in your_llm_stream(query):
            yield {"data": chunk}
            if await request.is_disconnected():
                break
    return EventSourceResponse(event_generator())
