# Source Inventory

## Interview Questions

| Website       | Content Type        | Estimated Chunks | Scraping Difficulty | Priority |
| ------------- | ------------------- | ---------------- | ------------------- | -------- |
| InterviewBit  | Interview Questions | 2,000–5,000      | Easy                | High     |
| GeeksforGeeks | Interview Questions | 3,000–8,000      | Easy                | High     |

---

## Job Descriptions

| Website       | Content Type     | Estimated Chunks | Scraping Difficulty | Priority |
| ------------- | ---------------- | ---------------- | ------------------- | -------- |
| LinkedIn Jobs | Job Descriptions | 500–2,000        | High                | Medium   |
| Indeed        | Job Descriptions | 1,000–3,000      | Medium              | High     |

---

## Technical Documentation

| Website                        | Content Type  | Estimated Chunks | Scraping Difficulty | Priority |
| ------------------------------ | ------------- | ---------------- | ------------------- | -------- |
| Apache Kafka Docs              | Documentation | 500–1,000        | Easy                | Medium   |
| Spring Boot Docs               | Documentation | 1,000–2,000      | Easy                | High     |
| Oracle Java Docs               | Documentation | 2,000–5,000      | Medium              | High     |
| Python Official Documentation  | Documentation | 4,000–6,000      | Easy                | High     |
| SQL Tutorial Documentation     | Documentation | 2,000–3,000      | Easy                | High     |
| Apache Spark Documentation     | Documentation | 3,000–5,000      | Medium              | High     |
| Apache Airflow Documentation   | Documentation | 2,000–4,000      | Medium              | Medium   |
| Machine Learning Documentation | Documentation | 4,000–6,000      | Medium              | High     |

---

## Interview Experiences

| Website     | Content Type          | Estimated Chunks | Scraping Difficulty | Priority |
| ----------- | --------------------- | ---------------- | ------------------- | -------- |
| Glassdoor   | Interview Experiences | 2,000–4,000      | High                | High     |
| AmbitionBox | Interview Experiences | 1,000–3,000      | High                | High     |

---

# Estimated Chunk Distribution

| Category              | Estimated Chunks  |
| --------------------- | ----------------- |
| Questions             | 10,000            |
| Job Descriptions      | 3,000             |
| Documentation         | 23,000–30,000     |
| Interview Experiences | 5,000             |
| **Total**             | **41,000–48,000** |

## Summary

The knowledge base will be built from four major source categories:

1. **Interview Questions** – Common DSA, System Design, and Technical Interview Questions.
2. **Job Descriptions** – Industry job requirements and skill expectations.
3. **Technical Documentation** – Official documentation for programming languages, frameworks, databases, and data engineering tools.
4. **Interview Experiences** – Real-world interview reports from candidates.

This source inventory is designed to generate approximately **41,000–48,000 chunks**, exceeding the faculty requirement of **40,000+ chunks** and providing sufficient coverage for the RAG-based AI Interview Simulator.

## Approved Architecture

```text
Knowledge Sources
        ↓
Raw Documents
        ↓
Cleaning
        ↓
Metadata Enrichment
        ↓
Recursive Chunking
        ↓
knowledge_base.csv
        ↓
Embeddings
        ↓
ChromaDB
        ↓
Retriever
        ↓
Agents
        ↓
Streamlit
```

**Architecture Status:** Frozen and approved. No further architectural changes will be made unless explicitly approved by the team.
