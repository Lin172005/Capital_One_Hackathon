# update_price_db.py
import os
import glob
import chromadb
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings

# --- Configuration ---
DB_PATH = "db"
PDF_REPORTS_PATH = "pdf_reports"  # Folder where your daily PDFs are saved
COLLECTION_NAME = "market_price_db"

def update_price_database():
    """
    Clears and re-ingests the latest market price PDF into a dedicated database.
    """
    print(f"--- Starting Market Price Database Update ---")

    # 1. Connect to ChromaDB
    client = chromadb.PersistentClient(path=DB_PATH)
    print(f"✅ Successfully connected to ChromaDB at: {DB_PATH}")

    # 2. Delete the old collection to ensure data is always fresh
    if COLLECTION_NAME in [c.name for c in client.list_collections()]:
        print(f"   - Deleting existing collection: '{COLLECTION_NAME}'")
        client.delete_collection(name=COLLECTION_NAME)
    
    # 3. Create a new, empty collection
    collection = client.create_collection(name=COLLECTION_NAME)
    print(f"   - Created new collection: '{COLLECTION_NAME}'")

    # 4. Find the newest PDF in the reports folder
    list_of_files = glob.glob(os.path.join(PDF_REPORTS_PATH, '*.pdf'))
    if not list_of_files:
        print(f"⚠️  WARNING: No PDF files found in '{PDF_REPORTS_PATH}'. The price database will be empty.")
        return
    
    latest_file = max(list_of_files, key=os.path.getctime)
    print(f"   - Found latest price report: {os.path.basename(latest_file)}")

    # 5. Load and process the latest PDF
    print("\n--- Loading and Processing Document ---")
    loader = PyPDFLoader(latest_file)
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    print(f"   - Split document into {len(texts)} chunks.")
        
    # 6. Generate embeddings and ingest into the new database
    print("\n--- Ingesting Data into ChromaDB ---")
    embeddings = OllamaEmbeddings(model="phi3", show_progress=True)
    
    collection.add(
        ids=[f"price_id{i}" for i in range(len(texts))],
        documents=[doc.page_content for doc in texts]
    )
    print("✅ Market price data ingestion complete.")

if __name__ == "__main__":
    update_price_database()