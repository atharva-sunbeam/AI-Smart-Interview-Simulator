# RAG Demo Workflow

## Purpose

This module demonstrates the Retrieval-Augmented Generation (RAG) retrieval process used in the AI-Powered Smart Interview Simulator.

The demonstration focuses on retrieving relevant context from ChromaDB before passing information to an LLM.

---

# Workflow

User Query
↓
Retriever
↓
Context Retrieval
↓
LLM Input

---

# Step 1: User Query

Example:

"What is inheritance in Python?"

The query represents a topic the user wants information about.

---

# Step 2: Retriever

The retriever converts the query into an embedding and searches the vector database.

Responsibilities:

* Semantic search
* Similarity matching
* Ranking relevant chunks

Example:

Query:

"What is inheritance in Python?"

↓

Search ChromaDB

---

# Step 3: Context Retrieval

Relevant chunks are retrieved.

Example:

Result 1:

"Inheritance allows a class to acquire properties and methods from another class."

Result 2:

"Python supports multiple inheritance through parent classes."

Result 3:

"Inheritance promotes code reuse and extensibility."

These chunks form the context supplied to the LLM.

---

# Step 4: LLM Input

The retrieved context is combined with the user query.

Example:

Context:

* Inheritance allows...
* Python supports multiple inheritance...

Question:
"What is inheritance in Python?"

↓

LLM

↓

Generated Answer

---

# Why RAG?

Without RAG:

User Query
↓
LLM Only
↓
Answer

Problems:

* Hallucinations
* Missing project-specific knowledge
* Less accurate responses

---

With RAG:

User Query
↓
Retriever
↓
Knowledge Base
↓
Relevant Context
↓
LLM
↓
Grounded Answer

Benefits:

* Higher accuracy
* Reduced hallucination
* Domain-specific knowledge
* Explainable retrieval process

---

# Integration with Project Architecture

Resume Upload
↓
Resume Parsing
↓
Skill Extraction
↓
Role Prediction
↓
RAG Retrieval
↓
Question Generation Agent
↓
Candidate Answer
↓
ML Answer Scoring
↓
LLM Feedback Agent
↓
Final Report

The RAG Demo module validates the retrieval layer before full integration with the Question Generation Agent and LLM pipeline.
