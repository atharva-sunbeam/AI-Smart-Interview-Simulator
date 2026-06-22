# Embedding Pipeline Design

## Purpose

Embeddings convert textual knowledge into numerical vector representations.

These vectors enable semantic search within the RAG system.

---

# Pipeline Flow

Knowledge Base

↓

Embedding Generation

↓

Vector Storage

↓

ChromaDB

↓

Retriever

↓

LLM

↓

Interview Simulator

---

# Input

datasets/processed/knowledge_base.csv

Contains:

* Chunk identifiers
* Metadata
* Chunk content

---

# Model

sentence-transformers/all-MiniLM-L6-v2

---

# Why This Model?

Advantages:

* Lightweight
* Fast inference
* Free and open source
* Strong semantic search performance
* Widely used in production RAG systems

---

# Embedding Generation Process

For each knowledge base record:

1. Read chunk content.
2. Generate vector embedding.
3. Associate embedding with chunk_id.
4. Store result.

Example:

Input:

"What is Python?"

Output:

[-0.123, 0.456, ..., 0.789]

---

# Output

datasets/processed/chunk_embeddings.pkl

Contains:

[
{
"chunk_id": "CHUNK000001",
"embedding": [...]
}
]

---

# Why Save Embeddings?

Pre-computed embeddings:

* Improve retrieval speed
* Avoid repeated model inference
* Reduce application latency

---

# Future Enhancements

Phase 1:

* Save embeddings as pickle

Phase 2:

* Store embeddings in ChromaDB

Phase 3:

* Metadata filtering

Phase 4:

* Hybrid retrieval

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
