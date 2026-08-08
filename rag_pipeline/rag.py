import os
import shutil
import pandas as pd
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

CHROMA_DIR = "vector_db/chroma"
CSV_PATH = "datasets/processed/knowledge_base.csv"

class RAGPipeline:
    def __init__(self):
        # Use lightweight local embedding model
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_store = None

    def initialize_db(self, force_recreate=False):
        """
        Loads knowledge_base.csv, chunks and indexes the data into ChromaDB.
        Self-heals if database directory is corrupted.
        """
        if not os.path.exists(CSV_PATH):
            print(f"[RAG Error] Processed database not found at {CSV_PATH}. Please compile first.")
            return False

        if os.path.exists(CHROMA_DIR) and not force_recreate:
            print("[RAG] Loading existing Chroma Vector Database...")
            try:
                self.vector_store = Chroma(
                    persist_directory=CHROMA_DIR,
                    embedding_function=self.embeddings
                )
                test_res = self.vector_store.similarity_search("python", k=1)
                if test_res:
                    return True
            except Exception as e:
                print(f"[RAG Warning] Failed to load existing Chroma DB: {e}. Re-building index...")
                force_recreate = True

        print("[RAG] Re-building Chroma Vector Database...")
        df = pd.read_csv(CSV_PATH)
        documents = []

        for _, row in df.iterrows():
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

        if os.path.exists(CHROMA_DIR):
            shutil.rmtree(CHROMA_DIR, ignore_errors=True)

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
        Filtered by candidate role and difficulty.
        """
        if self.vector_store is None:
            self.initialize_db()

        if role and difficulty:
            filter_dict = {"$and": [{"role": role}, {"difficulty": difficulty}]}
        elif role:
            filter_dict = {"role": role}
        elif difficulty:
            filter_dict = {"difficulty": difficulty}
        else:
            filter_dict = None

        if query:
            results = self.vector_store.similarity_search(
                query,
                k=k,
                filter=filter_dict
            )
        else:
            results = self.vector_store.similarity_search(
                f"Technical questions for {role}",
                k=k,
                filter=filter_dict
            )

        return [res.metadata for res in results]

    def add_session_to_knowledge_base(self, role, history_items):
        """
        Appends new session Q&A pairs to ChromaDB vector store for continuous learning.
        """
        if self.vector_store is None:
            self.initialize_db()

        new_docs = []
        for item in history_items:
            q = item.get("question")
            a = item.get("answer")
            topic = item.get("topic", "General")
            if q and a and len(a.strip()) > 10:
                page_content = f"Question: {q}\nAnswer: {a}"
                metadata = {
                    "role": role,
                    "topic": topic,
                    "difficulty": "Medium",
                    "question": q,
                    "answer": a
                }
                new_docs.append(Document(page_content=page_content, metadata=metadata))

        if new_docs and self.vector_store:
            try:
                self.vector_store.add_documents(new_docs)
                print(f"[RAG Continuous Learning] Added {len(new_docs)} new items to vector store.")
            except Exception as e:
                print(f"[RAG Continuous Learning Warning] {e}")

if __name__ == "__main__":
    rag = RAGPipeline()
    success = rag.initialize_db(force_recreate=True)
    if success:
        print("[Test] Database initialized successfully.")
        res = rag.retrieve_questions(role="Python Developer", difficulty="Hard", query="memory garbage collector", k=2)
        print(f"[Test] Retrieved {len(res)} results:")
        for idx, r in enumerate(res):
            print(f"  {idx+1}. Topic: {r['topic']} | Q: {r['question'][:60]}...")
