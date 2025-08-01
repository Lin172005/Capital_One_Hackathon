import os
import chromadb
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("Google AI API key not found. Please set the GOOGLE_API_KEY environment variable.")

# Configure the generative AI model
genai.configure(api_key=API_KEY)

# This is our sample document - our "knowledge base"
document_text = """
The Asian rice gall midge, known locally as 'Aanai Komban', is a significant pest affecting rice cultivation in Tamil Nadu. The primary symptom of an infestation is the appearance of long, silvery-white, hollow tubes, resembling onion leaves, instead of normal tillers. These are called 'silver shoots' or 'gall midge tubes'. The infestation prevents the formation of panicles, leading to a complete loss of yield from the affected tiller. For management, farmers are advised to use resistant rice varieties like MDU 5 and ADT 44. Additionally, applying Carbofuran 3G granules at a rate of 25 kg/ha in the nursery or 10 days after transplanting can effectively control the pest. Early detection and community-wide action are crucial for preventing widespread damage.
"""

# 1. INGESTION: Load the document into ChromaDB
print("Starting ingestion...")
client = chromadb.Client()
collection = client.get_or_create_collection(name="rice_knowledge_base")
collection.add(
    documents=[document_text],
    ids=["doc1"]
)
print("Ingestion complete.")


# 2. RETRIEVAL: Ask a question and find the relevant text
print("\nStarting retrieval...")
user_query = "What are the symptoms of Aanai Komban disease and how can I manage it?"

results = collection.query(
    query_texts=[user_query],
    n_results=1
)

retrieved_context = results['documents'][0][0]
print(f"Retrieved context: {retrieved_context}")


# 3. GENERATION: Use the retrieved context to generate an answer with the LLM
print("\nStarting generation...")

prompt_template = """
You are a helpful AI assistant for farmers. Answer the following question based ONLY on the provided context.
If the context doesn't contain the answer, say "I cannot answer this question based on the provided information."

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""
final_prompt = prompt_template.format(context=retrieved_context, question=user_query)

# NEW CODE
model = genai.GenerativeModel('gemini-1.5-flash-latest')
response = model.generate_content(final_prompt)

print("\n--- Final Answer ---")
print(response.text)
print("--------------------")