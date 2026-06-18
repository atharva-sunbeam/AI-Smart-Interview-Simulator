# InterviewBit Scraping Plan

## Objective

Collect Python interview questions and related technical interview content from InterviewBit for inclusion in the Smart Interview Simulator knowledge base.

---

## Target Pages

* Python Interview Questions
* Python Learning Resources
* Data Structures Interview Questions
* Algorithms Interview Questions
* SQL Interview Questions
* DBMS Interview Questions
* Operating System Interview Questions
* Computer Network Interview Questions
* System Design Interview Questions

---

## Expected Data

For each question:

* Question Title
* Question Statement
* Answer / Explanation
* Topic Category
* Difficulty Level (if available)
* Source URL

---

## Output File

Primary Output:

datasets/raw/python_questions.txt

Future Outputs:

* datasets/raw/sql_questions.txt
* datasets/raw/data_engineering.txt
* datasets/raw/ml_questions.txt

---

## Data Collection Flow

InterviewBit Page
↓
HTML Extraction
↓
Question Parsing
↓
Cleaning
↓
Deduplication
↓
Raw Dataset File

---

## Risks

### HTML Structure Changes

InterviewBit may update page layouts, causing selectors to fail.

### Duplicate Questions

The same question may appear in multiple categories.

### Missing Answers

Some pages may contain incomplete explanations.

### Rate Limiting

Large-scale crawling may trigger request restrictions.

### Content Quality Variations

Question formatting and answer depth may vary across pages.

---

## Success Criteria

* Collect Python interview questions successfully.
* Store data in structured text format.
* Remove duplicates.
* Preserve source URLs for traceability.
* Prepare data for chunking and knowledge-base ingestion.
