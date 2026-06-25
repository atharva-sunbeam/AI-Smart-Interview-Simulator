# Evaluation Integration

## Purpose

The Interview Session module now delegates answer evaluation to the Answer Evaluation Agent instead of using placeholder scores.

---

# Previous Workflow

Interview Session
↓

score = 8

↓

Fixed Score

Limitations:

* No Machine Learning
* No Explainability
* No Real Evaluation

---

# Updated Workflow

Interview Session
↓
Answer Evaluation Agent
↓
TF-IDF Vectorization
↓
Cosine Similarity
↓
Score + Feedback

---

# Evaluation Pipeline

Expected Answer
↓

Candidate Answer
↓

TF-IDF Vectorization
↓

Cosine Similarity
↓

Score
↓

Feedback

---

# Example

Expected Answer

Python is a high-level programming language.

Candidate Answer

Python is an interpreted programming language.

Output

```json
{
    "score": 82,
    "similarity": 0.82,
    "feedback": "Good understanding. Some details could be improved."
}
```

---

# Benefits

* Explainable AI
* Objective evaluation
* Machine Learning integration
* Easy future integration with LLM feedback

---

# Future Enhancements

Current:

TF-IDF
↓
Cosine Similarity

Future:

TF-IDF
↓
Keyword Coverage
↓
Random Forest Scoring
↓
LLM Feedback

---

# Updated Architecture

Streamlit UI
↓
System Controller
↓
Resume Parser
↓
Role Prediction
↓
Question Generation
↓
Interview Session
↓
Answer Evaluation Agent
↓
Report Generator
↓
JSON Report

```
```
