import os
import pandas as pd
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

CHROMA_DIR = "vector_db/chroma"
CSV_PATH = "datasets/processed/knowledge_base.csv"

class RAGPipeline:
    def __init__(self):
        # Use a lightweight, free local embedding model
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_store = None

    def initialize_db(self, force_recreate=False):
        """
        Loads knowledge_base.csv, chunks and indexes the data into ChromaDB.
        """
        if not os.path.exists(CSV_PATH):
            print(f"[RAG Error] Processed database not found at {CSV_PATH}. Please compile first.")
            return False

        # If Chroma database already exists and force_recreate is False, load it
        if os.path.exists(CHROMA_DIR) and not force_recreate:
            print("[RAG] Loading existing Chroma Vector Database...")
            self.vector_store = Chroma(
                persist_directory=CHROMA_DIR,
                embedding_function=self.embeddings
            )
            return True

        print("[RAG] Re-building Chroma Vector Database...")
        df = pd.read_csv(CSV_PATH)
        documents = []

        for _, row in df.iterrows():
            # Combine question and answer into the text to be embedded
            page_content = f"Question: {row['Question']}\nAnswer: {row['Answer']}"
            metadata = {
                "role": row["Role"],
                "topic": row["Topic"],
                "difficulty": row["Difficulty"],
                "question": row["Question"],
                "answer": row["Answer"]
            }
            doc = Document(page_content=page_content, metadata=metadata)
            documents.append(doc)

        # Clear existing Chroma dir if any
        if os.path.exists(CHROMA_DIR):
            import shutil
            shutil.rmtree(CHROMA_DIR)

        # Build Chroma db
        self.vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=CHROMA_DIR
        )
        print(f"[RAG] Successfully indexed {len(documents)} interview questions into ChromaDB.")
        return True

    def retrieve_questions(self, role, difficulty=None, query=None, k=5):
        """
        Retrieves matching questions from the vector database.
        Can be filtered by candidate role and difficulty.
        """
        if self.vector_store is None:
            self.initialize_db()

        # Build metadata filter for ChromaDB
        if role and difficulty:
            filter_dict = {"$and": [{"role": role}, {"difficulty": difficulty}]}
        elif role:
            filter_dict = {"role": role}
        elif difficulty:
            filter_dict = {"difficulty": difficulty}
        else:
            filter_dict = None

        if query:
            # Vector similarity search with filter
            results = self.vector_store.similarity_search(
                query,
                k=k,
                filter=filter_dict
            )
        else:
            # Fallback to general retrieval (matching filters)
            results = self.vector_store.similarity_search(
                f"Technical questions for {role}",
                k=k,
                filter=filter_dict
            )

        return [res.metadata for res in results]

if __name__ == "__main__":
    # Test execution
    rag = RAGPipeline()
    success = rag.initialize_db(force_recreate=True)
    if success:
        print("[Test] Database initialized successfully.")
        # Test query
        res = rag.retrieve_questions(role="Python Developer", difficulty="Hard", query="memory garbage collector", k=2)
        print(f"[Test] Retrieved {len(res)} results:")
        for idx, r in enumerate(res):
            print(f"  {idx+1}. Topic: {r['topic']} | Q: {r['question'][:60]}...")
