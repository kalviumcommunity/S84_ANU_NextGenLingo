NextGenLingo...
~ By Anu 🤍
Live Demo: [Next-Gen-Lingo](https://nextgenlingo-genai.netlify.app)

![NextGenLingo App Interface](https://drive.google.com/file/d/1GD0S78r5CiR8crDIuqYXqbYqeAeTZnJs/view?usp=sharing)
NextGenLingo is a custom-built conversational AI designed to be more than just a chatbot.
My goal was to create an intelligent agent that can understand and interact with documents, automate tasks, and even act as a personalized study tutor.

It uses Retrieval-Augmented Generation (RAG) to ground its answers in reliable sources, ensuring that when you ask a question about an uploaded PDF, the answers are accurate and come with citations. Beyond simple Q&A, I've integrated function-calling capabilities to let the AI interact with external tools, along with structured output to get information back in useful formats like JSON or Markdown tables.

`CORE FEATURES`  
Document Q&A with Sources: Upload a PDF and ask questions. The AI will analyze the text and provide answers with direct references to the source material.

Personalized Language Tutor: The agent can generate interactive quizzes, correct grammar, and provide tailored lessons on demand.

Task Automation: Ask the AI to schedule an event or fetch data from an API. It's designed to connect conversation to action.

Structured Data Output: Request information in specific formats like a JSON object or a Markdown table for easy use in other applications.

Contextual Memory: The agent remembers the flow of conversation, allowing for more natural and multi-step interactions.

`TECHNOLOGY`
Frontend: React (Vite) with Material-UI, deployed on Netlify.

Backend: Python with FastAPI, deployed on Render.

AI Engine: Built using modern LLMs and a vector database for the RAG pipeline.

`RUNNING LOCALLY`

Clone the repo:

git clone https://github.com/kalviumcommunity/S84_ANU_NextGenLingo.git
cd S84_ANU_NextGenLingo

     Setup Backend:

     Navigate to the **core** folder.

     Run pip install -r requirements.txt.

     Create a .env file and store API KEY like this ~ GEMINI_API_KEY

Setup Frontend:

     Run npm install in the root directory.

**Launch**:
Run **uvicorn api:app --reload** in the /core directory.
Run **npm run dev** in the root directory.