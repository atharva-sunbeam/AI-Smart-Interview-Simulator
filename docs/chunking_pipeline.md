# Chunking Pipeline Design

## Purpose

Chunking converts cleaned interview datasets into smaller knowledge units that can later be embedded and stored in a vector database.

Chunking is a critical step in the RAG pipeline because embeddings are generated from chunks rather than entire documents.

---

# Pipeline Flow

Raw Dataset

↓

Cleaning

↓

Clean Dataset

↓

Chunking

↓

Chunks

↓

Embeddings

↓

ChromaDB

↓

RAG Retrieval

---

# Current Strategy

Version 1 uses fixed-size chunking.

Each chunk contains a fixed number of cleaned records.

Current Configuration:

* Chunk Size: 5 records
* Overlap: None

---

# Chunk Creation Process

Input:

datasets/cleaned/python_questions_cleaned.txt

Output:

datasets/chunks/python_chunks.txt

---

# Example

Input:

What is Python?

Explain decorators.

What is inheritance?

What is polymorphism?

What is encapsulation?

What is abstraction?

Output:

Chunk 1

What is Python?

Explain decorators.

What is inheritance?

What is polymorphism?

What is encapsulation?

Chunk 2

What is abstraction?

---

# Why Chunking Is Required

Embeddings work best on smaller units of information.

Benefits:

* Faster retrieval
* Better relevance
* Lower storage overhead
* Improved RAG performance

---

# Future Enhancements

Phase 1:

* Fixed-size chunking

Phase 2:

* Recursive chunking

Phase 3:

* Metadata-aware chunking

Phase 4:

* Semantic chunking

---

# Final Goal

Clean Dataset

↓

Chunks

↓

Embeddings

↓

Vector Database

↓

Retriever

↓

Interview Simulator
