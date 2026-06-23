# Indexing Pipeline Design

## Purpose

The indexing pipeline loads embeddings and stores them inside ChromaDB.

This enables efficient semantic search during retrieval.

---

# Pipeline

Embeddings

↓

Prepare Documents

↓

Vector Database

↓

Indexed Knowledge Base

---

# Input

datasets/processed/chunk_embeddings.pkl

Contains:

* chunk_id
* content
* metadata
* embedding

---

# Process

1. Load serialized embeddings.
2. Extract:

   * IDs
   * Documents
   * Metadata
   * Vectors
3. Insert into ChromaDB collection.
4. Persist collection to disk.

---

# Output

ChromaDB Collection:

interview_knowledge_base

Stored inside:

chroma_db/

---

# Why Use ChromaDB?

Advantages:

* Persistent storage
* Fast similarity search
* Metadata filtering
* Scalable retrieval
* Open source

---

# Retrieval Flow

User Query

↓

Query Embedding

↓

ChromaDB Search

↓

Top K Results

↓

LLM

---

# Future Enhancements

* Metadata filtering
* Hybrid search
* Re-ranking
* Multi-collection support

---

# Final Goal

Knowledge Base

↓

Embeddings

↓

ChromaDB

↓

Retriever

↓

LLM

↓

AI Interview Simulator
