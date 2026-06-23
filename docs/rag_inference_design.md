# RAG Inference Design

## Purpose

The RAG Inference Module combines retrieval and generation into a single pipeline.

This module represents the first end-to-end implementation of Retrieval-Augmented Generation within the AI-Powered Smart Interview Simulator.

---

# Workflow

User Query
↓
Retriever
↓
Context Retrieval
↓
Generator
↓
Answer

---

# Step 1: User Query

Example:

"What are decorators in Python?"

The user submits a question.

---

# Step 2: Retriever

The retriever searches ChromaDB for relevant chunks.

Responsibilities:

* Semantic search
* Similarity matching
* Ranking relevant knowledge

Output:

Relevant chunks from the knowledge base.

---

# Step 3: Context Retrieval

Example Context:

"Decorators allow functions to modify the behavior of other functions."

"A decorator wraps another function without changing its source code."

The retrieved chunks become supporting context.

---

# Step 4: Generator

Current Version:

Mock generator.

Future Version:

Ollama + Mistral

Responsibilities:

* Consume retrieved context
* Generate grounded answers
* Reduce hallucinations

---

# Step 5: Answer

Example:

Question:
What are decorators in Python?

Answer:
Decorators are functions that extend the behavior of other functions without modifying their implementation.

---

# Why RAG?

Without Retrieval:

Question
↓
LLM
↓
Answer

Potential Issues:

* Hallucinations
* Missing domain knowledge
* Inconsistent answers

---

With RAG:

Question
↓
Retriever
↓
Knowledge Base
↓
Relevant Context
↓
Generator
↓
Answer

Benefits:

* Better accuracy
* Explainable retrieval
* Knowledge-grounded responses
* Easier debugging

---

# Future Evolution

Current:

Retriever
↓
Mock Generator

Next:

Retriever
↓
Ollama
↓
Mistral

Later:

Retriever
↓
Question Generation Agent
↓
Answer Evaluation Agent
↓
Feedback Agent

---

# Project Architecture Position

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
Recommendation Engine
↓
Final Report

The RAG Inference Module serves as the foundation for all future LLM-powered interactions in the system.
