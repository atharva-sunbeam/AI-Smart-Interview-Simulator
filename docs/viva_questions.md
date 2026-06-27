# Viva Questions and Answers

## AI Smart Interview Simulator

---

# Machine Learning Questions

## Q1. Why did you choose Logistic Regression?

**Answer:**

We used Logistic Regression for the role prediction module because it is a lightweight, interpretable, and efficient supervised classification algorithm.

Reasons:

* Works well for text classification.
* Fast to train and predict.
* Produces a strong baseline for resume classification.
* Easy to explain during technical interviews.
* Performs effectively when combined with TF-IDF features.

In our project, resume text is converted into numerical feature vectors using TF-IDF, and Logistic Regression predicts the most suitable job role such as:

* Python Developer
* Data Engineer
* ML Engineer
* Data Analyst

---

## Q2. Why did you use TF-IDF?

**Answer:**

Machine learning models cannot process raw text directly. TF-IDF converts resume text into numerical vectors.

TF-IDF measures:

* **Term Frequency (TF):** Importance of a word in a document.
* **Inverse Document Frequency (IDF):** Reduces the weight of very common words.

Advantages:

* Lightweight
* Fast
* Interpretable
* Excellent baseline for text classification

Example:

Resume:

Python SQL Kafka Spark

becomes a numerical feature vector that can be used by the classifier.

---

## Q3. Why did you use Cosine Similarity?

**Answer:**

Cosine Similarity compares the semantic closeness between the expected answer and the candidate's answer.

Pipeline:

Expected Answer

↓

TF-IDF Vectorization

↓

Cosine Similarity

↓

Similarity Score

Advantages:

* Simple and explainable.
* Independent of answer length.
* Suitable for short technical answers.
* Easy to interpret during demonstrations.

Example:

Expected:

Python is an interpreted programming language.

Candidate:

Python is a high-level interpreted language.

The similarity score will be high because the vectors are close.

---

# RAG Questions

## Q4. What is RAG?

**Answer:**

RAG stands for **Retrieval-Augmented Generation**.

Instead of asking the LLM to answer using only its pretrained knowledge, the system first retrieves relevant information from a knowledge base.

Pipeline:

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

Generated Answer

Benefits:

* Reduces hallucinations.
* Produces domain-specific answers.
* Uses project-specific knowledge.

---

## Q5. Why did you choose ChromaDB?

**Answer:**

ChromaDB is a lightweight vector database designed for AI applications.

Reasons:

* Local deployment
* Persistent storage
* Metadata filtering
* Easy Python integration
* Fast semantic search
* Suitable for academic projects

It stores embeddings of knowledge-base chunks and enables efficient retrieval.

---

## Q6. Why are embeddings required?

**Answer:**

Embeddings convert text into dense numerical vectors that capture semantic meaning.

Unlike keyword search, embeddings allow semantic retrieval.

Example:

Question:

Explain OOP.

Knowledge Base:

Object-Oriented Programming concepts...

Although the exact words differ, embeddings identify the semantic similarity.

---

# System Design Questions

## Q7. Explain the complete architecture.

**Answer:**

The project combines Machine Learning, Retrieval-Augmented Generation (RAG), Large Language Models, and a modular multi-agent architecture.

Workflow:

Resume Upload

↓

Resume Parser

↓

Role Prediction (ML)

↓

Question Generation (RAG)

↓

Interview Session

↓

Answer Evaluation (ML)

↓

Report Generation

↓

JSON Report

Future versions will integrate an LLM to generate dynamic interview questions and qualitative feedback.

---

## Q8. How does data flow through the system?

**Answer:**

1. The candidate uploads a resume.
2. The Resume Parser extracts and cleans the text.
3. The Role Prediction model predicts the target job role.
4. The RAG pipeline retrieves relevant knowledge from ChromaDB.
5. The Question Generation Agent generates interview questions.
6. The candidate submits answers.
7. The Answer Evaluation Agent computes similarity scores.
8. The Report Generator produces a structured JSON report.

---

## Q9. How does retrieval work?

**Answer:**

Retrieval pipeline:

Knowledge Sources

↓

Cleaning

↓

Chunking

↓

Embeddings

↓

ChromaDB

↓

Retriever

↓

Relevant Context

↓

Question Generation Agent

The retriever searches the vector database for semantically similar chunks instead of relying on exact keyword matches.

---

# Project Questions

## Q10. What challenges did you face?

**Answer:**

Some key challenges included:

* Collecting high-quality interview datasets.
* Cleaning and chunking heterogeneous data sources.
* Designing a scalable RAG pipeline.
* Integrating independently developed modules.
* Maintaining consistent interfaces between agents.
* Managing Git branches and resolving merge conflicts.

---

## Q11. Why not use only ChatGPT?

**Answer:**

Using only a general-purpose LLM has several limitations:

* It may hallucinate information.
* It cannot reliably answer using project-specific data.
* It lacks explainable scoring.
* It does not perform role prediction.

Our project combines traditional ML with RAG and LLMs:

* ML predicts the candidate's role.
* RAG retrieves relevant technical knowledge.
* ML evaluates candidate answers.
* LLMs (planned) enhance question generation and qualitative feedback.

This hybrid architecture is more accurate, explainable, and suitable for technical interviews.

---

## Q12. What genuine ML components are implemented?

**Answer:**

The project includes multiple machine learning components:

### Role Prediction

* TF-IDF Vectorization
* Logistic Regression Classifier

Purpose:

Predicts the most suitable technical role from resume content.

---

### Answer Evaluation

* TF-IDF Vectorization
* Cosine Similarity

Purpose:

Evaluates candidate answers against expected answers and generates an explainable score.

---

### Future ML Enhancements

* Resume Skill Extraction using spaCy.
* Difficulty Prediction using Logistic Regression.
* Improved Answer Scoring using Random Forest.
* Recommendation Engine based on weak topic analysis.

---

# Final Viva Summary

## Key Technologies

* Python
* Streamlit
* Scikit-learn
* LangChain
* ChromaDB
* Sentence Transformers
* PyPDF2
* Joblib
* Ollama (planned)

---

## Project Highlights

* Machine Learning based Role Prediction.
* Retrieval-Augmented Generation (RAG).
* Explainable ML Answer Evaluation.
* Modular Multi-Agent Architecture.
* ChromaDB Vector Database.
* Automated Interview Report Generation.

---

## Final One-Line Project Description

**AI Smart Interview Simulator is a hybrid system that combines traditional Machine Learning, Retrieval-Augmented Generation (RAG), and a modular multi-agent architecture to conduct role-specific technical interviews, evaluate candidate responses using explainable ML techniques, and generate structured interview reports.**
