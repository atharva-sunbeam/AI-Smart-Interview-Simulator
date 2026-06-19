# Source Collection Strategy

## Purpose

This document defines the recommended order for collecting data sources for the AI-Powered Smart Interview Simulator knowledge base.

The collection strategy prioritizes sources that provide high-value content, large datasets, and lower collection complexity.

---

# Collection Order

## 1. InterviewBit

### Why First?

* High-quality interview questions.
* Well-structured content.
* Easy scraping complexity.
* Covers Python, SQL, DSA, System Design, and CS fundamentals.
* Provides immediate value for the interview simulator.

Expected Contribution:

* 2,000–5,000 records.

---

## 2. GeeksforGeeks

### Why Second?

* Very large collection of interview questions.
* Broad topic coverage.
* Publicly accessible content.
* Complements InterviewBit with additional explanations and examples.

Expected Contribution:

* 3,000–8,000 records.

---

## 3. GitHub Repositories

### Why Third?

* Open-source interview preparation resources.
* Curated question collections.
* Structured markdown content.
* Easy access and low collection barriers.

Example Sources:

* Tech Interview Handbook
* Coding Interview University
* Awesome Interview Questions

Expected Contribution:

* 2,500–5,000 records.

---

## 4. Technical Documentation

### Why Fourth?

* Provides authoritative technical knowledge.
* Supports Retrieval-Augmented Generation (RAG).
* Covers concepts beyond interview questions.

Example Sources:

* Python Documentation
* Oracle Java Documentation
* Apache Kafka Documentation
* Apache Spark Documentation
* Apache Airflow Documentation
* Spring Boot Documentation

Expected Contribution:

* 23,000–30,000 records.

---

## 5. Job Descriptions

### Why Fifth?

* Helps identify industry skill requirements.
* Enables role-specific interview preparation.
* Supports resume-job matching features.

Sources:

* Indeed
* LinkedIn Jobs

Expected Contribution:

* 3,000 records.

---

## 6. Interview Experiences

### Why Sixth?

* Most difficult to collect.
* Often contains noisy and unstructured data.
* Valuable but lower priority than core knowledge sources.
* Useful for company-specific interview preparation.

Sources:

* Glassdoor
* AmbitionBox

Expected Contribution:

* 5,000 records.

---

# Strategy Summary

| Priority Order | Source Category         | Reason                                      |
| -------------- | ----------------------- | ------------------------------------------- |
| 1              | InterviewBit            | High-quality structured interview questions |
| 2              | GeeksforGeeks           | Large interview dataset                     |
| 3              | GitHub Repositories     | Open-source curated content                 |
| 4              | Technical Documentation | Authoritative technical knowledge           |
| 5              | Job Descriptions        | Industry requirements and skills            |
| 6              | Interview Experiences   | Valuable but difficult to collect           |

This strategy maximizes knowledge-base growth while minimizing early-stage collection complexity and project risk.
