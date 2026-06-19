# Cleaning Pipeline Design

## Purpose

The cleaning pipeline improves dataset quality before chunking, embedding generation, and RAG ingestion.

Poor quality data results in:

* Poor retrieval
* Duplicate embeddings
* Irrelevant interview questions

---

# Pipeline Flow

Raw Data

↓

Validation

↓

Cleaning

↓

Clean Dataset

---

# Cleaning Operations

## Remove Empty Lines

Removes blank records that do not contain useful information.

Example:

Before:

Question 1

(blank line)

Question 2

After:

Question 1

Question 2

---

## Remove Duplicates

Removes repeated questions.

Example:

What is Python?

What is Python?

After:

What is Python?

---

## Remove Short Entries

Removes very short entries that are unlikely to be useful interview questions.

Example:

PDF

Home

Login

These are typically navigation or UI elements rather than interview content.

---

# Output

Input:

datasets/raw/python_questions.txt

Output:

datasets/cleaned/python_questions_cleaned.txt

---

# Future Enhancements

Sprint 9+

* Remove navigation text
* Remove category headings
* Remove advertisements
* Normalize punctuation
* Standardize capitalization
* Near-duplicate detection

---

# Final Goal

Raw Dataset

↓

Clean Dataset

↓

Chunking

↓

Knowledge Base

↓

Embeddings

↓

ChromaDB

↓

RAG
