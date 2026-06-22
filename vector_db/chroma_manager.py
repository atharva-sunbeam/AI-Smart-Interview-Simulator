"""
ChromaDB Manager

Purpose:
Manage storage and retrieval of knowledge-base
embeddings using ChromaDB.
"""

import chromadb

class ChromaManager:

    
    COLLECTION_NAME = "interview_knowledge_base"

    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = None

    def create_collection(self):
        """
        Create or load collection.
        """
        self.collection = self.client.get_or_create_collection(
            name=self.COLLECTION_NAME
        )
        return self.collection

    def add_documents(
        self,
        ids,
        documents,
        embeddings=None,
        metadatas=None,
    ):
        """
        Add documents to ChromaDB.
        """

        if self.collection is None:
            self.create_collection()

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def count_documents(self):
        """
        Return total documents in collection.
        """

        if self.collection is None:
            self.create_collection()

        return self.collection.count()

    def search_documents(self, query_text, n_results=5):
        """
        Semantic search.
        """

        if self.collection is None:
            self.create_collection()

        return self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
        )
    

if __name__ == "__main__":
    manager = ChromaManager()
    manager.create_collection()

    
    print(
        f"Collection '{manager.COLLECTION_NAME}' initialized."
    )
    
