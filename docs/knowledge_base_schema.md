# Knowledge Base Schema Design

## Purpose

The knowledge base is the central dataset used by the RAG pipeline.

All collected data sources such as:

* Interview Questions
* Technical Documentation
* Job Descriptions
* Interview Experiences

will be cleaned, chunked, and stored in a unified format.

Each row in `knowledge_base.csv` represents a single chunk of text.

---

# Data Flow

Web Scraping
↓
Raw Documents
↓
Cleaning
↓
Metadata Enrichment
↓
Chunking
↓
knowledge_base.csv
↓
Embeddings
↓
ChromaDB
↓
RAG Retrieval

---

# Recommended Schema

| Column Name      | Required | Description                                                                               |
| ---------------- | -------- | ----------------------------------------------------------------------------------------- |
| chunk_id         | Yes      | Unique identifier for each chunk                                                          |
| document_id      | Yes      | Original document identifier                                                              |
| source_type      | Yes      | Type of source (interview_question, technical_doc, job_description, interview_experience) |
| role             | Yes      | Target role (Python Developer, Data Engineer, ML Engineer, Data Analyst)                  |
| topic            | Yes      | Main topic category                                                                       |
| subtopic         | No       | Detailed classification within topic                                                      |
| difficulty       | No       | Easy, Medium, Hard                                                                        |
| experience_level | No       | Fresher, Junior, Mid-Level                                                                |
| content          | Yes      | Actual chunk text                                                                         |
| keywords         | No       | Searchable keywords                                                                       |
| tags             | No       | Additional metadata tags                                                                  |
| source_title     | No       | Title of original source                                                                  |
| source_url       | No       | Original source URL                                                                       |
| chunk_index      | Yes      | Position of chunk in original document                                                    |
| total_chunks     | Yes      | Total chunks generated from source document                                               |
| embedding_status | No       | pending, generated, failed                                                                |

---

# Source Types

Supported values:

* interview_question
* technical_doc
* job_description
* interview_experience
* roadmap
* blog
* github_repository

---

# Supported Roles

* Python Developer
* Data Engineer
* Machine Learning Engineer
* Data Analyst

Future roles can be added without schema changes.

---

# Example Chunk Metadata

Document:

"Kafka Architecture Guide"

After chunking:

Document ID: DOC_KAFKA_001

Chunks:

* CHUNK_KAFKA_001
* CHUNK_KAFKA_002
* CHUNK_KAFKA_003

All chunks share the same document_id while maintaining unique chunk_id values.

---

# Why This Schema?

## RAG Compatibility

Supports vector database ingestion and metadata filtering.

## Scalability

Can handle 40,000+ chunk records.

## Traceability

Every chunk can be linked back to its original source.

## Interview Simulation

Supports role-based and topic-based retrieval for generating relevant interview questions.

---

# Final Decision

Each row in knowledge_base.csv will represent one chunk of text, not one document.

This aligns with industry-standard RAG architectures and improves retrieval quality.
