# Resume Parsing Design

## Purpose

The Resume Parser extracts useful information from a candidate's resume.

The extracted information will later be used for:

* Skill Identification
* Role Prediction
* Interview Personalization
* Question Generation

---

# Pipeline

PDF Resume

↓

Text Extraction

↓

Text Cleaning

↓

Skill Extraction

---

# Step 1: PDF Text Extraction

Technology:

PyPDF2

Purpose:

Extract textual content from uploaded resumes.

Input:

resume.pdf

Output:

Raw resume text

---

# Step 2: Text Cleaning

Operations:

* Convert to lowercase
* Remove special characters
* Remove extra whitespace

Purpose:

Standardize text for downstream NLP processing.

---

# Step 3: Skill Extraction

Current Approach:

Keyword Matching

Example Skills:

* Python
* SQL
* Spark
* Kafka
* Airflow
* Machine Learning

Purpose:

Identify candidate technologies from resume content.

---

# Future Enhancements

Phase 1:

Keyword Matching

Phase 2:

spaCy Named Entity Recognition (NER)

Phase 3:

ML-based Skill Classification

---

# Final Output

Example:

```python
[
    "python",
    "sql",
    "spark",
    "airflow"
]
```

These extracted skills will later be used by:

* Role Prediction Model
* RAG Retrieval
* Interview Question Generation

---

# Final Architecture

Resume PDF

↓

Resume Parser

↓

Extracted Skills

↓

ML Role Prediction

↓

RAG Interview System
