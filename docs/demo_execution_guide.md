# Demo Execution Guide

# Purpose

This guide explains how to run the AI Smart Interview Simulator for demonstration and evaluation.

---

# Prerequisites

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Run Demo (CLI)

Execute:

```bash
python scripts/demo_run.py
```

Expected Output:

* Predicted Role
* Generated Interview Question
* Candidate Answer
* Evaluation Score
* Similarity Score
* Feedback
* Interview Report

---

# Run Streamlit Application

Start the web interface:

```bash
streamlit run frontend/app.py
```

The application allows users to:

* Upload Resume
* Predict Role
* Start Interview
* Answer Questions
* View Final Report

---

# Run Unit Tests

Run all tests:

```bash
pytest
```

Run a specific module:

```bash
pytest tests/test_answer_evaluation_agent.py -v
```

---

# Expected Demo Flow

Resume Upload

↓

Resume Parsing

↓

Role Prediction (ML)

↓

Question Generation

↓

Candidate Answer

↓

Answer Evaluation (TF-IDF + Cosine Similarity)

↓

Interview Report Generation

↓

JSON Report

---

# Faculty Demonstration Flow

1. Upload a sample resume.
2. Display the predicted role.
3. Generate interview questions.
4. Submit candidate answers.
5. Show ML-based evaluation.
6. Display generated interview report.
7. Explain the architecture.

---

# Technologies Demonstrated

* Resume Parsing
* NLP
* TF-IDF Vectorization
* Logistic Regression
* RAG Architecture
* ChromaDB
* Cosine Similarity
* JSON Report Generation

---

# Expected Project Architecture

Streamlit UI

↓

System Controller

↓

Resume Parser

↓

Role Prediction Model

↓

Question Generation Agent

↓

Interview Session

↓

Answer Evaluation Agent

↓

Report Generator

↓

JSON Report
