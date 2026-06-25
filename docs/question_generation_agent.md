# Question Generation Agent Design

## Purpose

The Question Generation Agent creates technical interview questions tailored to a candidate's profile.

The generated questions are role-specific and leverage contextual knowledge retrieved from the RAG system.

---

# Architecture

Predicted Role

↓

RAG Retrieval

↓

Context Collection

↓

Prompt Construction

↓

Question Generation

---

# Input

Example:

Python Developer

---

# Step 1: Role Identification

The system receives the predicted role from the Role Prediction Model.

Example:

* Python Developer
* Data Engineer
* ML Engineer
* Data Analyst

---

# Step 2: RAG Retrieval

Relevant knowledge chunks are retrieved from the vector database.

Example:

Python decorators

Generators

Context managers

---

# Step 3: Prompt Construction

The retrieved context is combined with candidate role information.

Example:

Role:
Python Developer

Context:
Python decorators modify function behavior.

---

# Step 4: Question Generation

Current Version:

Mock question generation.

Future Version:

Ollama + Mistral LLM.

---

# Example Output

Role:

Python Developer

Generated Question:

Explain decorators in Python.

---

# Future Enhancements

Phase 1:

Mock Question Generation

Phase 2:

Ollama Integration

Phase 3:

Adaptive Question Generation

Phase 4:

Multi-turn Conversational Interviews

---

# Final Architecture

Resume

↓

Role Prediction

↓

Question Generation Agent

↓

Interview Question

↓

Candidate Answer
