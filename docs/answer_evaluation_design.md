# Answer Evaluation Design

## Purpose

The Answer Evaluation Agent provides an explainable machine learning approach for scoring candidate responses during interviews.

Unlike pure LLM-based scoring, this approach produces measurable similarity scores using NLP techniques.

---

# Workflow

Expected Answer
↓
Vectorization
↓
Cosine Similarity
↓
Score
↓
Feedback

---

# Step 1: Expected Answer

Reference answer stored in the knowledge base.

Example:

"Python is a high-level interpreted programming language."

---

# Step 2: Candidate Answer

User response submitted during the interview.

Example:

"Python is an interpreted programming language."

---

# Step 3: TF-IDF Vectorization

Convert both answers into numerical vectors.

Example:

Expected Answer
↓
TF-IDF Vector

Candidate Answer
↓
TF-IDF Vector

Benefits:

* Lightweight
* Fast
* Interpretable
* Suitable for text comparison

---

# Step 4: Cosine Similarity

Measure similarity between vectors.

Formula:

Cosine Similarity = cos(θ)

Output Range:

0.0 → Completely different

1.0 → Identical meaning

Example:

Similarity = 0.78

Score = 78

---

# Step 5: Feedback Generation

Score Ranges:

| Score  | Feedback                |
| ------ | ----------------------- |
| 80-100 | Excellent understanding |
| 60-79  | Good understanding      |
| 40-59  | Partial understanding   |
| 0-39   | Weak answer             |

---

# Why This Approach?

Advantages:

* Explainable AI
* Fast evaluation
* Objective scoring
* Easy to justify in interviews
* Demonstrates actual ML usage

---

# Future Improvements

Current:

TF-IDF
↓
Cosine Similarity

Future:

TF-IDF Features
↓
Random Forest Regressor
↓
Predicted Interview Score

Additional Features:

* Keyword Match Score
* Technical Term Count
* Answer Length
* Semantic Similarity

---

# Project Integration

Question Generation Agent
↓
Expected Answer
↓
Candidate Answer
↓
Answer Evaluation Agent
↓
Score
↓
LLM Feedback Agent
↓
Final Report

This module satisfies the project's requirement for a genuine, explainable ML component and complements the RAG-based interview system.
