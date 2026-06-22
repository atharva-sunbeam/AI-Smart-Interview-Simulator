"""
RAG Retrieval Demonstration

Purpose:
Demonstrate the retrieval stage of the RAG pipeline.

Flow:

Query
↓
Retriever
↓
Retrieve Context
↓
Display Results
"""

from vector_db.chroma_manager import ChromaManager

def retrieve_context(query: str, n_results: int = 3):
    manager = ChromaManager()
    manager.create_collection()

    
    results = manager.search_documents(
        query_text=query,
        n_results=n_results,
    )

    return results
    

def print_results(results):
    print("\nRetrieved Context:\n")


    documents = results.get("documents", [])

    if not documents:
        print("No documents found.")
        return

    for i, document in enumerate(documents[0], start=1):
        print(f"{i}.")
        print(document)
        print()
    

if __name__ == "__main__":
    query = "What is inheritance in Python?"

print(f"\nQuery: {query}")

results = retrieve_context(query)

print_results(results)

