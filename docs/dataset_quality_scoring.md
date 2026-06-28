# Dataset Quality Scoring

## Purpose

The Dataset Quality Engine improves the quality of collected technical datasets before they are used for Retrieval-Augmented Generation (RAG).

---

# Processing Pipeline

Raw Dataset

↓

HTML Cleaning

↓

Short Answer Removal

↓

Low Score Filtering

↓

Quality Scoring

↓

Knowledge Base

---

# Quality Score Formula

Final Score =

Question Quality (25)

+

Answer Quality (35)

+

Stack Overflow Score (30)

+

Accepted Answer Bonus (10)

Maximum Score = 100

---

# Filtering Thresholds

Minimum Question Length:

15 characters

Minimum Answer Length:

50 characters

Minimum Stack Overflow Score:

5

Minimum Quality Score:

60

---

# Example

Question:

What is Python?

Answer:

Python is a high-level interpreted programming language.

Stack Overflow Score:

120

Accepted Answer:

Yes

Final Quality Score:

92.5

---

# Benefits

- Removes noisy records
- Improves embedding quality
- Enhances semantic retrieval
- Produces better RAG responses
- Improves answer evaluation