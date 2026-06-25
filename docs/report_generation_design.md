# Report Generation Design

## Purpose

The Report Generator combines outputs from different modules into a structured interview report.

The report summarizes the candidate's interview performance and provides recommendations for improvement.

---

# Workflow

Resume Upload
↓
Resume Parsing
↓
Role Prediction
↓
Question Generation
↓
Interview Session
↓
Answer Evaluation
↓
Report Generator
↓
Interview Report (JSON)

---

# Report Fields

| Field           | Description                              |
| --------------- | ---------------------------------------- |
| Candidate Name  | Candidate's name                         |
| Predicted Role  | Role predicted by the ML model           |
| Questions Asked | Interview questions presented            |
| Scores          | Individual question scores               |
| Average Score   | Overall interview score                  |
| Strengths       | Areas where the candidate performed well |
| Weaknesses      | Areas requiring improvement              |
| Recommendations | Suggested topics for further study       |

---

# Example Output

```json
{
    "candidate_name": "John Doe",
    "predicted_role": "Data Engineer",
    "questions_asked": [
        "What is Python?",
        "Explain Kafka."
    ],
    "scores": [
        82,
        76
    ],
    "average_score": 79.0,
    "strengths": [
        "Strong Python knowledge"
    ],
    "weaknesses": [
        "Needs Kafka practice"
    ],
    "recommendations": [
        "Study Kafka architecture"
    ]
}
```

---

# Why JSON?

Advantages:

* Lightweight
* Human-readable
* Easy to parse
* Compatible with web applications
* Easy to convert to PDF or dashboards later

---

# Future Enhancements

* PDF report generation
* Charts and score visualizations
* Historical interview reports
* Performance trends
* Downloadable report in Streamlit

---

# Integration

Resume Parser
↓
Role Prediction
↓
RAG Question Generation
↓
Answer Evaluation Agent
↓
LLM Feedback Agent
↓
Report Generator
↓
Interview Report

The Report Generator serves as the final stage of the AI-Powered Smart Interview Simulator by consolidating all interview outcomes into a single structured report.
