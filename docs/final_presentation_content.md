# Final Presentation Content

# Slide 1 — Title Slide

## AI-Powered Smart Interview Simulator

Team Members:

* Atharva Birje
* Shreyas Deshingkar

Technology Stack:

* Python
* Machine Learning
* RAG
* ChromaDB
* Streamlit

---

# Slide 2 — Problem Statement

Traditional interview preparation systems:

* Are generic.
* Lack personalization.
* Do not adapt to candidate skills.
* Provide limited feedback.

Need:

An intelligent and personalized interview simulator.

---

# Slide 3 — Objectives

* Automate technical interview preparation.
* Predict candidate role automatically.
* Generate role-specific questions.
* Evaluate candidate answers.
* Provide detailed feedback.

---

# Slide 4 — Existing System

Limitations:

* Static question banks.
* No personalization.
* Manual evaluation.
* No AI assistance.

---

# Slide 5 — Proposed System

Features:

* Resume-based role prediction.
* AI-powered question generation.
* RAG-based retrieval.
* Automated answer evaluation.
* Interactive Streamlit interface.

---

# Slide 6 — System Architecture

Present architecture diagram.

```text
Resume
↓
Parser
↓
Role Prediction
↓
Question Generation
↓
Retriever
↓
ChromaDB
↓
Evaluation
↓
Report
```

---

# Slide 7 — Technology Stack

Frontend:

* Streamlit

Backend:

* Python

ML:

* Scikit-learn

Embeddings:

* Sentence Transformers

Vector Database:

* ChromaDB

Testing:

* Pytest

Version Control:

* Git & GitHub

---

# Slide 8 — Machine Learning Models Used

Role Prediction:

* TF-IDF
* Logistic Regression

Answer Evaluation:

* TF-IDF Similarity

Embedding Model:

* all-MiniLM-L6-v2

---

# Slide 9 — RAG Pipeline

```text
User Query
      ↓
Embedding Generation
      ↓
ChromaDB Search
      ↓
Top-K Retrieval
      ↓
Question Generation
```

Benefits:

* Context-aware questions.
* Improved relevance.
* Personalized interviews.

---

# Slide 10 — System Demonstration

Demonstrate:

1. Resume Upload
2. Skill Extraction
3. Role Prediction
4. Question Generation
5. Answer Submission
6. Evaluation
7. Report Generation

---

# Slide 11 — Results

Achievements:

* Complete end-to-end pipeline.
* RAG integration.
* Automated evaluation.
* 36/36 tests passing.

---

# Slide 12 — Future Scope

* LLM Integration (Mistral/Llama)
* Speech-to-Text Interviews
* Text-to-Speech Interviewer
* Adaptive Question Generation
* Cloud Deployment
* User Authentication
* Dashboard Analytics

---

# Slide 13 — Conclusion

The AI Smart Interview Simulator successfully automates and personalizes technical interview preparation using Machine Learning and Retrieval-Augmented Generation techniques.

---

# Slide 14 — Thank You

Questions?

```
```
