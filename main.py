# main.py (Final Version with Automated Lifespan and All Features)
import os
import shutil
import chromadb
import google.generativeai as genai
import ollama
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import Optional, Dict
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from fastapi.concurrency import run_in_threadpool
from contextlib import asynccontextmanager
import httpx

# --- PyTorch Imports ---
import torch
import torchvision.transforms as transforms
from PIL import Image
import io

# --- Import your automation scripts ---
from save_page_as_pdf import save_page_as_pdf
from update_price_db import update_price_database

# --- Global state to hold our database connections ---
db_connections: Dict[str, chromadb.Collection] = {}

# --- NEW: Lifespan Manager for Startup and Shutdown ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This code runs ONCE when the server starts up
    print("--- Running startup data refresh process ---")
    try:
        print("   - Step 1: Downloading latest price PDF...")
        save_page_as_pdf()
        
        print("\n   - Step 2: Updating the market price database...")
        update_price_database()
        
        print("\n--- Startup data refresh process finished successfully! ---")
    except Exception as e:
        print(f"❌ ERROR during startup data refresh: {e}")

    # --- Connect to ChromaDB AFTER data refresh is complete ---
    print("\nConnecting to ChromaDB collections...")
    client = chromadb.PersistentClient(path="db")
    db_connections["rice_collection"] = client.get_collection(name="rice_knowledge_base")
    db_connections["price_collection"] = client.get_collection(name="market_price_db")
    print("✅ Successfully connected to both ChromaDB collections.")
    
    yield  # The application is now running
    
    # This code runs ONCE when the server shuts down
    print("\n--- Server shutting down ---")
    db_connections.clear()


# --- Basic Setup with the new lifespan manager ---
app = FastAPI(title="Namma Uzhavan Nanban API", lifespan=lifespan)
load_dotenv()


# --- Load your offline PyTorch model ---
try:
    MODEL_PATH = 'models/paddy_disease_classifier.pt' 
    OFFLINE_DISEASE_MODEL = torch.jit.load(MODEL_PATH, map_location=torch.device('cpu')) 
    OFFLINE_DISEASE_MODEL.eval()
    CLASS_NAMES = ['bacterial_leaf_blight', 'bacterial_leaf_streak', 'bacterial_panicle_blight', 'blast', 'brown_spot', 'dead_heart', 'downy_mildew', 'hispa', 'normal', 'tungro']
    print("✅ Successfully loaded local PyTorch disease model.")
    image_transforms = transforms.Compose([
        transforms.Resize(256), transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    print("   - Image transformation pipeline created.")
except Exception as e:
    OFFLINE_DISEASE_MODEL = None
    print(f"⚠️ WARNING: Could not load local PyTorch model. Error: {e}")

# --- Pydantic Models ---
class Location(BaseModel): latitude: float; longitude: float
class QueryRequest(BaseModel): question: str; location: Optional[Location] = None

# --- API/DB Configuration ---
try:
    API_KEY = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=API_KEY)
    text_model = genai.GenerativeModel('gemini-1.5-flash-latest')
    print("✅ Gemini Models configured.")
except Exception as e:
    print(f"⚠️ Warning: Could not configure Google AI. {e}")

# --- Helper Function for Live Weather ---
async def get_weather_data(lat: float, lon: float):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            if response.status_code == 200:
                data = response.json().get('current', {})
                return {"current_temp": data.get('temperature_2m'), "humidity": data.get('relative_humidity_2m')}
    except Exception: return None

# --- API Endpoints ---
@app.post("/api/text-query")
async def handle_text_query(request: QueryRequest):
    user_query_tamil = request.question
    rag_context = ""
    live_context = ""
    try:
        english_query = (await run_in_threadpool(text_model.generate_content, f"Translate to English: '{user_query_tamil}'")).text.strip()
        
        if request.location and (weather_data := await get_weather_data(request.location.latitude, request.location.longitude)):
            if weather_data.get('current_temp') is not None:
                live_context = f"\n\nCURRENT WEATHER DATA:\n- Temperature: {weather_data['current_temp']}°C\n- Humidity: {weather_data['humidity']}%"

        price_keywords = ['price', 'rate', 'market', 'cost', 'deal', 'mandi', 'விலை', 'சந்தை']
        if any(keyword in english_query.lower() for keyword in price_keywords):
            print("   - Price keyword detected. Querying market price database.")
            price_results = db_connections["price_collection"].query(query_texts=[english_query], n_results=5, include=["documents"])
            rag_context += "\n\n--- LATEST MARKET PRICES ---\n" + "\n\n".join(price_results['documents'][0])

        print("   - Querying main rice knowledge base.")
        rice_results = db_connections["rice_collection"].query(query_texts=[english_query], n_results=3, include=["documents"])
        rag_context += "\n\n--- RICE KNOWLEDGE BASE ---\n" + "\n\n".join(rice_results['documents'][0])
        
        final_prompt = f"""You are "Namma Uzhavan Nanban," an AI expert for farmers. A farmer asked in Tamil: '{user_query_tamil}'.
        Based ONLY on the combined context below, answer in Tamil. Prioritize LIVE WEATHER DATA or LATEST MARKET PRICES if relevant.
        ---
        COMBINED CONTEXT:\n{live_context or ""}{rag_context}
        ---
        YOUR DETAILED TAMIL ANSWER:"""

        response = await run_in_threadpool(text_model.generate_content, final_prompt)
        return {"answer": response.text, "source": "Gemini (Hybrid RAG)"}
    except Exception as e:
        print(f"Main handler error: {e}")
        return {"answer": "An error occurred with the online model.", "source": "Error"}

@app.post("/api/offline-query")
async def handle_offline_query_with_rag(request: QueryRequest):
    try:
        context = "\n\n---\n\n".join(db_connections["rice_collection"].query(query_texts=[request.question], n_results=4, include=["documents"])['documents'][0])
        prompt = f"""Based ONLY on the context, answer the user's question. CONTEXT:\n{context}\nQUESTION:\n"{request.question}"\nANSWER:"""
        response = await run_in_threadpool(ollama.chat, model='phi3', messages=[{'role': 'user', 'content': prompt}])
        return {"answer": response['message']['content'], "source": "Ollama (Offline)"}
    except Exception as e:
        print(f"Error during offline RAG query: {e}")
        return {"answer": "An error occurred with the local model.", "source": "Error"}

@app.post("/api/image-diagnosis")
async def handle_image_diagnosis(image: UploadFile = File(...)):
    if not OFFLINE_DISEASE_MODEL: return {"answer": "Local model not loaded.", "source": "Error"}
    try:
        contents = await image.read()
        pil_image = Image.open(io.BytesIO(contents)).convert('RGB')
        image_tensor = image_transforms(pil_image).unsqueeze(0)
        with torch.no_grad():
            outputs = OFFLINE_DISEASE_MODEL(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted_idx = torch.max(probabilities, 1)
        
        predicted_class = CLASS_NAMES[predicted_idx.item()]
        confidence_percent = confidence.item() * 100
        print(f"Online Diagnosis: Predicted '{predicted_class}' with {confidence_percent:.2f}% confidence.")
        context = "\n\n---\n\n".join(db_connections["rice_collection"].query(query_texts=[f"remedy for {predicted_class}"], n_results=3, include=["documents"])['documents'][0])
        generation_prompt = f"""A farmer's crop is '{predicted_class}' ({confidence_percent:.2f}% confidence). Based on the context, provide a detailed treatment plan in Tamil.
        ENGLISH CONTEXT:\n{context}\nDETAILED TAMIL TREATMENT PLAN:"""
        final_response = await run_in_threadpool(text_model.generate_content, generation_prompt)
        return {"answer": final_response.text, "source": "Local Model + Gemini"}
    except Exception as e:
        print(f"Error during hybrid diagnosis: {e}")
        return {"answer": "An error occurred during diagnosis.", "source": "Error"}

@app.post("/api/offline-image-diagnosis")
async def handle_offline_image_diagnosis(image: UploadFile = File(...)):
    if not OFFLINE_DISEASE_MODEL: return {"answer": "Offline model not available.", "source": "Error"}
    try:
        contents = await image.read()
        pil_image = Image.open(io.BytesIO(contents)).convert('RGB')
        image_tensor = image_transforms(pil_image).unsqueeze(0)
        with torch.no_grad():
            outputs = OFFLINE_DISEASE_MODEL(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted_idx = torch.max(probabilities, 1)
        
        predicted_class = CLASS_NAMES[predicted_idx.item()]
        confidence_percent = confidence.item() * 100
        print(f"Offline Prediction: {predicted_class} with {confidence_percent:.2f}% confidence.")
        context = "\n\n---\n\n".join(db_connections["rice_collection"].query(query_texts=[f"remedy for {predicted_class}"], n_results=3, include=["documents"])['documents'][0])
        final_prompt = f"""You are an agricultural expert. Based ONLY on the context, create a clear, step-by-step remedy plan for '{predicted_class}'. Use simple language and markdown.
        CONTEXT:\n{context}\nTREATMENT PLAN:"""
        response = await run_in_threadpool(ollama.chat, model='phi3', messages=[{'role': 'user', 'content': final_prompt}])
        final_answer = f"**I am confident this is {predicted_class} ({confidence_percent:.2f}%).**\n\n{response['message']['content']}"
        return {"answer": final_answer, "source": "Local PyTorch Model + Phi-3"}
    except Exception as e:
        print(f"Error during offline diagnosis: {e}")
        return {"answer": "An error occurred with the local model.", "source": "Error"}

# --- Serve the Frontend ---
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
@app.get("/")
async def read_root():
    return FileResponse('frontend/index.html')