"""
RAG Inference Pipeline

Purpose:
End-to-end Retrieval-Augmented Generation (RAG).

Pipeline:

User Query
↓
Retriever
↓
Context Retrieval
↓
Prompt Construction
↓
Generator
↓
Answer
"""

from vector_db.chroma_manager import ChromaManager

class RAGInference:


    def __init__(self):
        self.retriever = ChromaManager()
        self.retriever.create_collection()

    def retrieve_context(
        self,
        query: str,
        n_results: int = 3,
    ):
        """
        Retrieve relevant documents from ChromaDB.
        """

        results = self.retriever.search_documents(
            query_text=query,
            n_results=n_results,
        )

        documents = results.get("documents", [])

        if not documents or not documents[0]:
            return []

        return documents[0]

    def build_prompt(
        self,
        query: str,
        context,
    ):
        """
        Build prompt for generator.
        """

        context_text = "\n".join(context)

        return f"""
    ```

    Question:
    {query}

    Context:
    {context_text}

    Answer:
    """

    
    def generate_answer(
        self,
        query: str,
        context,
    ):
        """
        Mock LLM response.

        Replace with Ollama/Mistral later.
        """

        context_text = "\n".join(context)

        return f"""
    

    Question:
    {query}

    Context:
    {context_text}

    Answer:
    Generated answer placeholder.
    """

    
    def run(
        self,
        query: str,
    ):
        """
        Complete RAG workflow.
        """

        context = self.retrieve_context(query)

        answer = self.generate_answer(
            query=query,
            context=context,
        )

        return {
            "query": query,
            "context": context,
            "answer": answer,
        }
    

if __name__ == "__main__":


    rag = RAGInference()

    result = rag.run(
        "What is inheritance in Python?"
    )

    print(result["answer"])

