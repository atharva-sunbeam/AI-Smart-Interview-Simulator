# Final System Architecture

## Overview

The AI Smart Interview Simulator is an end-to-end intelligent interview platform that analyzes a candidate's resume, predicts the most suitable technical role, generates interview questions using RAG, evaluates candidate answers, and produces a final interview report.

---

# High-Level Architecture

```text
Resume Upload
        ↓
Resume Parser
        ↓
Skill Extraction
        ↓
Role Prediction Model
        ↓
Question Generation Agent
        ↓
Retriever
        ↓
ChromaDB
        ↓
Interview Session
        ↓
Answer Evaluation Agent
        ↓
Report Generator
        ↓
Streamlit UI
```

---

# Module Interactions

## 1. Resume Parser

Responsibilities:

* Extract text from uploaded PDF resumes.
* Clean and preprocess extracted text.
* Extract technical skills using keyword matching.

Output:

```text
Resume Text + Extracted Skills
```

---

## 2. Role Prediction Model

Responsibilities:

* Convert resume text into TF-IDF features.
* Predict the candidate's most suitable technical role.

Supported Roles:

* Python Developer
* Data Engineer
* ML Engineer
* Data Analyst

Output:

```text
Predicted Role
```

---

## 3. Question Generation Agent

Responsibilities:

* Receive predicted role.
* Query the Retriever.
* Generate role-specific interview questions.

Output:

```text
Question + Expected Answer
```

---

## 4. Retriever

Responsibilities:

* Convert user query into embeddings.
* Perform semantic similarity search.
* Retrieve relevant knowledge chunks.

Output:

```text
Top-K Relevant Chunks
```

---

## 5. ChromaDB

Responsibilities:

* Store embeddings.
* Perform vector similarity search.
* Enable efficient RAG retrieval.

Stored Data:

* Chunk ID
* Content
* Metadata
* Embeddings

---

## 6. Interview Session

Responsibilities:

* Coordinate complete interview workflow.
* Manage session state.
* Store interview history.

Maintains:

* Current Role
* Current Question
* Candidate Answer
* Session History

---

## 7. Answer Evaluation Agent

Responsibilities:

* Compare candidate answer with expected answer.
* Compute similarity score.
* Generate feedback.

Output:

```text
Score + Feedback
```

---

## 8. Report Generator

Responsibilities:

* Aggregate interview results.
* Generate final report.

Output:

```text
Average Score
Detailed Feedback
Interview Summary
```

---

# Data Flow

```text
PDF Resume
      ↓
Resume Parsing
      ↓
Resume Text
      ↓
Skill Extraction
      ↓
Role Prediction
      ↓
Role
      ↓
Question Generation
      ↓
Retriever
      ↓
ChromaDB Search
      ↓
Context Retrieval
      ↓
Interview Question
      ↓
Candidate Answer
      ↓
Answer Evaluation
      ↓
Report Generation
```

---

# Technology Stack

## Frontend

* Streamlit

## Backend

* Python

## Machine Learning

* Scikit-learn
* TF-IDF
* Logistic Regression

## NLP

* Sentence Transformers
* Transformers

## Vector Database

* ChromaDB

## Data Processing

* Pandas
* NumPy

## Testing

* Pytest

## PDF Processing

* PyPDF2

## Version Control

* Git
* GitHub

```
```
