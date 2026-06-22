# Metadata Design

## Purpose

The Metadata Builder is responsible for generating structured metadata for every chunk stored in the knowledge base.

Metadata improves:

* Searchability
* Filtering
* Retrieval quality
* Source traceability
* Future analytics

---

# Metadata Flow

Raw Documents
↓
Cleaning
↓
Chunking
↓
Metadata Builder
↓
chunk_metadata.csv
↓
Embeddings
↓
ChromaDB

---

# Metadata Fields

| Field       | Description                                              |
| ----------- | -------------------------------------------------------- |
| chunk_id    | Unique identifier for a chunk                            |
| document_id | Unique identifier for the source document                |
| source_type | Type of source (question, documentation, JD, experience) |
| topic       | Domain/topic (Python, SQL, ML, etc.)                     |
| content     | Chunk text content                                       |

---

# Example Record

| chunk_id    | document_id | source_type        | topic  | content         |
| ----------- | ----------- | ------------------ | ------ | --------------- |
| CHUNK000001 | DOC000001   | interview_question | python | What is Python? |

---

# ID Generation Strategy

## Chunk IDs

Format:

CHUNK000001

CHUNK000002

CHUNK000003

Purpose:
Provide a unique identifier for every chunk.

---

## Document IDs

Format:

DOC000001

DOC000002

DOC000003

Purpose:
Group chunks belonging to the same source document.

---

# Source Types

Supported values:

* interview_question
* technical_documentation
* job_description
* interview_experience

---

# Topics

Examples:

* python
* sql
* data_engineering
* machine_learning
* java
* kafka
* spark
* airflow

---

# Output File

Location:

datasets/processed/chunk_metadata.csv

Example:

chunk_id,document_id,source_type,topic,content
CHUNK000001,DOC000001,interview_question,python,"What is Python?"

---

# Benefits for RAG

Metadata enables:

* Topic-based retrieval
* Source filtering
* Faster debugging
* Improved search relevance
* Better traceability of generated responses

The metadata layer is a foundational component of the knowledge-base pipeline and will be used before embedding generation and vector database storage.
