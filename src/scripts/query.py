import os
import chromadb
import google.generativeai as genai
from dotenv import load_dotenv

# --- Constants ---
COLLECTION_NAME = "rice_knowledge_base"

def setup_model():
    """Configure and set up the generative model."""
    load_dotenv()
    API_KEY = os.getenv("GOOGLE_API_KEY")
    if not API_KEY:
        raise ValueError("Google AI API key not found.")
    genai.configure(api_key=API_KEY)
    return genai.GenerativeModel('gemini-1.5-flash-latest')

def main():
    """
    Main function to run the query engine.
    """
    model = setup_model()

    print("Connecting to the knowledge base...")
    # NEW CODE
    client = chromadb.PersistentClient(path="db")
    try:
        collection = client.get_collection(name=COLLECTION_NAME)
        print("Connection successful.")
    except Exception as e:
        print(f"Error connecting to collection: {e}")
        print(f"Please make sure you have run the ingest.py script first.")
        return

    # Main loop to ask questions
    while True:
        user_query = input("\nAsk a question about rice disease or finance (or type 'exit' to quit): ")
        if user_query.lower() == 'exit':
            break

        # 1. RETRIEVAL
        results = collection.query(
            query_texts=[user_query],
            n_results=3,  # Retrieve top 3 most relevant chunks
            include=["documents", "metadatas"]
        )

        retrieved_context = "\n\n---\n\n".join(results['documents'][0])
        source_files = list(set(meta['source'] for meta in results['metadatas'][0]))

        # 2. GENERATION
        prompt_template = """
        You are a helpful AI assistant for farmers in Tamil Nadu. Answer the following question based ONLY on the provided context.
        Cite the source document names you used to answer the question.
        If the context doesn't contain the answer, say "I cannot answer this question based on the provided information."

        CONTEXT:
        {context}

        QUESTION:
        {question}

        ANSWER:
        """
        final_prompt = prompt_template.format(context=retrieved_context, question=user_query)

        print("\nGenerating answer...")
        response = model.generate_content(final_prompt)

        # Print the final answer and sources
        print("\n--- Answer ---")
        print(response.text)
        print("\n--- Sources ---")
        for source in source_files:
            print(f"- {source}")
        print("----------------")

if __name__ == "__main__":
    main()