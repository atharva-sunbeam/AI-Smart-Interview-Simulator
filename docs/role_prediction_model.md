# Role Prediction Model

## Purpose

The Role Prediction Model identifies the most suitable technical role for a candidate based on resume content.

This module introduces Machine Learning into the Smart Interview Simulator and enables role-specific interview generation.

---

# Architecture

Resume Upload
↓
Resume Parsing
↓
Skill Extraction (spaCy NLP)
↓
Resume Text
↓
TF-IDF Vectorization
↓
Random Forest Classifier
↓
Predicted Role

---

# Why Role Prediction?

Different roles require different interview questions.

Examples:

### Python Developer

Focus Areas:

* Python
* OOP
* APIs
* Django / Flask

---

### Data Engineer

Focus Areas:

* SQL
* Kafka
* Spark
* Airflow
* ETL Pipelines

---

### ML Engineer

Focus Areas:

* Machine Learning
* Deep Learning
* Feature Engineering
* Model Deployment

---

### Data Analyst

Focus Areas:

* SQL
* Excel
* Statistics
* Power BI
* Tableau

---

# Input Features

Resume information:

* Skills
* Projects
* Certifications
* Experience
* Technical Keywords

Example:

Python, SQL, Kafka, Spark, Airflow

---

# NLP Processing

Tool:

spaCy

Tasks:

* Tokenization
* Named Entity Recognition
* Skill Extraction
* Text Normalization

---

# Machine Learning Pipeline

Resume Text
↓
TF-IDF Vectorization
↓
Feature Matrix
↓
Random Forest Classifier
↓
Predicted Role

---

# Why TF-IDF?

TF-IDF converts resume text into numerical features.

Benefits:

* Lightweight
* Interpretable
* Fast training
* Effective for text classification

---

# Why Random Forest?

Benefits:

* Handles high-dimensional features
* Robust to noise
* Easy to explain during interviews
* Strong baseline classifier

---

# Evaluation Metrics

* Accuracy
* Precision
* Recall
* F1 Score

Target:

Accuracy > 80%

---

# Output

Example:

Input Resume:

Python
SQL
Kafka
Spark
Airflow

Predicted Role:

Data Engineer

---

# Integration with Interview System

Predicted Role
↓
RAG Retrieval
↓
Question Generation Agent
↓
Role-Specific Interview

This ensures that generated interview questions match the candidate's profile and career path.
