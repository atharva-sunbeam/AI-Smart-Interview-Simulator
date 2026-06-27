# Stack Overflow Data Pipeline

## Purpose

Collect high-quality technical interview knowledge using the official Stack Exchange API.

---

# Data Source

Stack Exchange API

Website:

https://api.stackexchange.com

---

# Target Topics

* Python
* SQL
* Machine Learning
* Apache Kafka
* Apache Spark

---

# Data Collection Flow

Stack Exchange API

↓

Question Retrieval

↓

Data Filtering

↓

CSV Dataset

↓

Cleaning

↓

Chunking

↓

Knowledge Base

↓

Embeddings

↓

ChromaDB

---

# Collected Fields

* Question
* Answer
* Tags
* Score
* Accepted Answer
* URL

---

# Filtering Strategy

Questions are filtered using:

* Relevant tags
* Highest voted questions
* Accepted answers
* Technical topics only

This improves overall knowledge quality.

---

# API Rate Limits

The Stack Exchange API applies request limits.

Strategies used:

* Pagination
* Limited page size
* Sequential requests
* Retry after failures (future enhancement)

---

# Data Quality

Collected questions are expected to have:

* Clear technical titles
* Relevant programming tags
* Community voting
* Accepted answers where available

---

# Future Improvements

* Retrieve complete answer bodies.
* Download comments.
* Remove duplicate questions.
* Automatically classify difficulty.
* Enrich metadata for RAG retrieval.
