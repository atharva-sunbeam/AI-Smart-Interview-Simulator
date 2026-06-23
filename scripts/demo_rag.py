"""
RAG Demonstration Script
"""

from rag_pipeline.rag_inference import RAGInference

def main():

    
    query = "What are decorators in Python?"

    rag = RAGInference()

    result = rag.run(query)

    print("\nQuery:")
    print(query)

    print("\nRetrieved Context:")

    if result["context"]:
        for i, chunk in enumerate(
            result["context"],
            start=1,
        ):
            print(f"\n{i}. {chunk}")
    else:
        print("No context found.")

    print("\nGenerated Answer:")
    print(result["answer"])
    

if __name__ == "__main__":
    main()
