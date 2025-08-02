import os
import chromadb
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# --- Constants ---
# Path to the directory where you've saved your downloaded documents
DATA_PATH = "data/raw"
# ChromaDB collection name
COLLECTION_NAME = "rice_knowledge_base"


def load_documents(directory_path):
    """
    Loads all .txt and .pdf documents from a directory and its subdirectories.
    """
    print(f"Loading documents from {directory_path}...")
    documents = []
    # Use os.walk to go through all subdirectories
    for root, _, files in os.walk(directory_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                if filename.endswith('.pdf'):
                    print(f"  - Reading PDF: {filename}")
                    reader = PdfReader(file_path)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() or ""
                    documents.append({"page_content": text, "metadata": {"source": filename}})
                elif filename.endswith('.txt'):
                    print(f"  - Reading TXT: {filename}")
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                    documents.append({"page_content": text, "metadata": {"source": filename}})
            except Exception as e:
                print(f"    - Error reading {filename}: {e}")
                continue
    print(f"Loaded {len(documents)} documents successfully.")
    return documents

def split_text_into_chunks(documents):
    """
    Splits the loaded documents into smaller chunks for better processing.
    """
    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.create_documents(
        texts=[doc["page_content"] for doc in documents],
        metadatas=[doc["metadata"] for doc in documents]
    )
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks

def store_chunks_in_chromadb(chunks):
    """
    Stores the text chunks into the ChromaDB vector store.
    """
    print("Storing chunks into ChromaDB...")
    # NEW CODE
    client = chromadb.PersistentClient(path="db")

    # Clear out the old collection if it exists, to ensure a fresh start
    try:
        if COLLECTION_NAME in [c.name for c in client.list_collections()]:
            client.delete_collection(name=COLLECTION_NAME)
            print(f"Cleared old collection: {COLLECTION_NAME}")
    except Exception as e:
        print(f"Error clearing collection: {e}")

    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    documents_to_add = [chunk.page_content for chunk in chunks]
    metadatas_to_add = [chunk.metadata for chunk in chunks]
    ids_to_add = [f"{chunk.metadata['source']}_{i}" for i, chunk in enumerate(chunks)]

    collection.add(
        documents=documents_to_add,
        metadatas=metadatas_to_add,
        ids=ids_to_add
    )
    print("Successfully stored chunks in ChromaDB.")
    print(f"Total chunks in collection: {collection.count()}")

def main():
    """
    Main function to run the ingestion pipeline.
    """
    print("--- Starting Knowledge Base Ingestion Pipeline ---")
    raw_documents = load_documents(DATA_PATH)
    if raw_documents:
        text_chunks = split_text_into_chunks(raw_documents)
        store_chunks_in_chromadb(text_chunks)
    else:
        print("No documents found in the data directory. Exiting.")
    print("--- Ingestion Pipeline Complete ---")

if __name__ == "__main__":
    main()