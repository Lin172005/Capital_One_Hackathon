import os
import shutil
import chromadb
import google.generativeai as genai
import ollama
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from fastapi.concurrency import run_in_threadpool

# --- Basic Setup ---
app = FastAPI(title="Namma Uzhavan Nanban API (Our Farmer's Friend)")
load_dotenv()

# --- Pydantic Models ---
class QueryRequest(BaseModel):
    question: str

# --- Online Models and DB Connection ---
try:
    API_KEY = os.getenv("GOOGLE_API_KEY")
    if API_KEY:
        genai.configure(api_key=API_KEY)
    text_model = genai.GenerativeModel('gemini-1.5-flash-latest')
    vision_model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    print(f"Warning: Could not configure Google AI. {e}")

try:
    client = chromadb.PersistentClient(path="db")
    collection = client.get_collection(name="rice_knowledge_base")
    print("Successfully connected to ChromaDB.")
except Exception as e:
    print(f"Fatal Error connecting to ChromaDB: {e}")
    exit()

# --- API Endpoints ---

@app.post("/api/offline-query")
async def handle_offline_query_with_rag(request: QueryRequest):
    # This simplified offline endpoint now expects ENGLISH input
    user_query_english = request.question

    try:
        results = collection.query(query_texts=[user_query_english], n_results=4, include=["documents"])
        retrieved_context = "\n\n---\n\n".join(results['documents'][0])

        final_prompt = f"""You are an expert agricultural assistant. Based ONLY on the following context, answer the user's question.

        CONTEXT:\n---\n{retrieved_context}\n---\n
        QUESTION:\n"{user_query_english}"\n
        ANSWER:"""
        
        response = await run_in_threadpool(
            ollama.chat,
            model='phi3',
            messages=[{'role': 'user', 'content': final_prompt}]
        )
        
        return {"answer": response['message']['content'], "source": "Ollama (Offline)"}

    except Exception as e:
        print(f"Error during offline RAG query: {e}")
        return {"answer": "An error occurred with the local model.", "source": "Error"}


@app.post("/api/text-query")
async def handle_text_query(request: QueryRequest):
    user_query_tamil = request.question
    try:
        # We assume online queries can be in Tamil, as Gemini can handle it.
        # First, we translate the Tamil query to English for better search results.
        translation_prompt = f"Translate the following to English: '{user_query_tamil}'"
        english_query_response = text_model.generate_content(translation_prompt)
        user_query_english = english_query_response.text.strip()

        results = collection.query(query_texts=[user_query_english], n_results=3, include=["documents"])
        context = "\n\n---\n\n".join(results['documents'][0])
        
        prompt = f"""You are a helpful AI assistant. A user asked a question in Tamil: '{user_query_tamil}'.
        Based only on the English context provided, please answer the question in the Tamil language.

        ENGLISH CONTEXT:\n{context}\n
        TAMIL ANSWER:"""

        response = await run_in_threadpool(text_model.generate_content, prompt)
        return {"answer": response.text, "source": "Gemini (Online)"}
    except Exception as e:
        return {"answer": "An error occurred with the online model.", "source": "Error"}


@app.post("/api/image-diagnosis")
async def handle_image_diagnosis(image: UploadFile = File(...)):
    def process_image_sync():
        temp_image_path = f"temp_{image.filename}"
        try:
            with open(temp_image_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            
            uploaded_file = genai.upload_file(path=temp_image_path)
            vision_prompt = "You are an expert in rice crop diseases. Analyze this image and identify the specific disease. Respond with only the name of the disease (e.g., 'Rice Blast'). If unsure, respond 'Unknown'."
            response = vision_model.generate_content([vision_prompt, uploaded_file])
            disease_name = response.text.strip()
            genai.delete_file(uploaded_file.name)
            
            if "Unknown" in disease_name or not disease_name:
                return {"answer": "மன்னிக்கவும், படத்திலிருந்து நோயை என்னால் அடையாளம் காண முடியவில்லை. வேறு படத்தை முயற்சிக்கவும்.", "source": "Gemini Vision"}
            
            query = f"what is the remedy for {disease_name}"
            results = collection.query(query_texts=[query], n_results=3, include=["documents"])
            context = "\n\n---\n\n".join(results['documents'][0])
            
            generation_prompt = f"""A farmer has shown an image that you identified as '{disease_name}'. Based on the following English context, provide a detailed treatment and management plan in the Tamil language.

                ENGLISH CONTEXT:\n{context}\n
                TAMIL ANSWER:
            """
            final_response = text_model.generate_content(generation_prompt)
            return {"answer": final_response.text, "source": "Gemini Vision"}
        finally:
            if os.path.exists(temp_image_path):
                os.remove(temp_image_path)

    return await run_in_threadpool(process_image_sync)

# --- Serve the Frontend ---
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse('frontend/index.html')