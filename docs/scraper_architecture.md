# Scraper Architecture Design

## Purpose

The scraping module is responsible for collecting raw data from multiple online sources and preparing it for the data processing pipeline.

The collected data will later pass through:

Web Scraping

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

↓

RAG

To avoid code duplication and improve maintainability, all scraper implementations will inherit from a common base class.

---

# Class Hierarchy

```text
BaseScraper
    |
    +-- InterviewQuestionScraper
    |
    +-- JobDescriptionScraper
    |
    +-- DocumentationScraper
    |
    +-- ExperienceScraper
```

---

# BaseScraper

## Purpose

BaseScraper provides a common framework for all scraping modules.

Every scraper in the project should inherit from this class.

This ensures:

* Consistent architecture
* Code reuse
* Easier maintenance
* Standardized workflow

---

## Common Methods

### fetch_page()

Responsibility:

* Send requests to websites
* Retrieve page content

Output:

* Raw webpage content

---

### parse_content()

Responsibility:

* Extract useful information
* Remove unnecessary page elements

Output:

* Structured content

---

### clean_text()

Responsibility:

* Remove unwanted text
* Remove extra spaces
* Standardize formatting

Output:

* Clean text data

---

### save_data()

Responsibility:

* Save processed data

Possible formats:

* TXT
* CSV
* JSON

Output:

* Dataset files

---

# InterviewQuestionScraper

## Purpose

Collect interview questions from:

* InterviewBit
* GeeksforGeeks
* GitHub repositories

---

## Output Examples

* python_questions.txt
* sql_questions.txt
* ml_questions.txt
* data_engineer_questions.txt

---

# JobDescriptionScraper

## Purpose

Collect job descriptions for:

* Data Engineer
* Data Analyst
* Python Developer
* Machine Learning Engineer

---

## Benefits

Provides:

* Required skills
* Industry expectations
* Tool requirements
* Common responsibilities

---

## Output Examples

* data_engineer_jobs.txt
* python_developer_jobs.txt
* ml_engineer_jobs.txt

---

# DocumentationScraper

## Purpose

Collect technical documentation and learning resources.

Examples:

* Python Documentation
* Kafka Documentation
* Spark Documentation
* SQL Documentation
* Airflow Documentation

---

## Benefits

Provides high-quality technical knowledge for:

* RAG retrieval
* Answer evaluation
* Follow-up question generation

---

## Output Examples

* python_docs.txt
* kafka_docs.txt
* spark_docs.txt

---

# ExperienceScraper

## Purpose

Collect interview experience reports.

Examples:

* Amazon Data Engineer Interview Experience
* TCS Python Interview Experience
* Infosys Data Analyst Interview Experience

---

## Benefits

Provides:

* Real interview patterns
* Company-specific questions
* Difficulty insights

---

## Output Examples

* amazon_de_experiences.txt
* tcs_python_experiences.txt

---

# Data Flow

Each scraper follows the same workflow:

```text
Website
   ↓
fetch_page()
   ↓
parse_content()
   ↓
clean_text()
   ↓
save_data()
   ↓
Raw Dataset
```

---

# Advantages of This Architecture

## Reusability

Common functionality is defined once and reused by all scraper classes.

---

## Maintainability

Changes can be made centrally in BaseScraper.

---

## Scalability

New scraper types can be added without changing the overall architecture.

Examples:

* BlogScraper
* GitHubRepositoryScraper
* DocumentationAPIScraper

---

## Consistency

All scraper implementations follow the same lifecycle and structure.

---

# Future Expansion

In future sprints, specialized scraper classes will override the methods inherited from BaseScraper and implement source-specific scraping logic.

Examples:

* InterviewBit scraper
* GeeksforGeeks scraper
* LinkedIn job scraper
* Documentation scraper

---

# Final Decision

All scraping modules will inherit from BaseScraper.

This architecture provides a scalable, maintainable, and reusable foundation for building the data collection layer of the AI-Powered Smart Interview Simulator.
