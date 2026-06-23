# Retriever Design

## Purpose

The Retriever is the core component of the RAG pipeline.

It retrieves the most relevant knowledge chunks based on a user's query.

---

# Pipeline

User Query

↓

Query Embedding

↓

Vector Similarity Search

↓

Top K Results

↓

LLM Context

---

# Input

Example:

"Explain Python decorators"

---

# Process

1. Convert query into embedding vector.
2. Compare query embedding with stored chunk embeddings.
3. Compute cosine similarity scores.
4. Select top K most relevant chunks.
5. Format chunks as context for the LLM.

---

# Similarity Metric

Cosine Similarity

Formula:

similarity(A, B)

Higher similarity score indicates greater semantic relevance.

---

# Output

Example:

[
"Decorators allow functions to modify behavior...",
"Python decorators are implemented using @ syntax..."
]

---

# Why Retrieval Is Important

Retrieval enables:

* Context-aware responses
* Reduced hallucinations
* Domain-specific knowledge access

---

# Final RAG Flow

User Query

↓

Retriever

↓

Relevant Context

↓

LLM

↓

Interview Question / Feedback
