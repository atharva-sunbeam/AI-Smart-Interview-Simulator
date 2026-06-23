# Role Prediction Model

## Purpose

Predict a candidate's most suitable technical role based on resume skills and keywords.

---

# Architecture

Resume Skills
↓
TF-IDF Vectorization
↓
Logistic Regression
↓
Predicted Role

---

# Supported Roles

1. Python Developer
2. Data Engineer
3. ML Engineer
4. Data Analyst

---

# Input

Example Resume Skills:

Python
SQL
Spark
Kafka
Airflow

---

# TF-IDF Vectorization

Converts resume text into numerical features.

Example:

Input:

Python SQL Spark Kafka

Output:

[0.24, 0.12, 0.45, ...]

Benefits:

* Lightweight
* Fast
* Interpretable
* Effective for text classification

---

# Logistic Regression

Classifier used to predict the most likely role.

Reasons:

* Simple baseline model
* Fast training
* Easy to explain in interviews
* Works well with TF-IDF features

---

# Example Prediction

Input:

Python SQL Spark Kafka Airflow ETL

Output:

Data Engineer

---

# Evaluation

Metrics:

* Accuracy
* Precision
* Recall
* F1 Score

Target:

80%+ accuracy

---

# Integration

Resume
↓
Skill Extraction (spaCy)
↓
Role Prediction
↓
RAG Retrieval
↓
Question Generation Agent

Role prediction enables personalized interview questions aligned with the candidate's skill set.
