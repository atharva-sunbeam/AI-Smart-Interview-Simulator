# Project Workflow

## End-to-End Workflow

```text
User Upload Resume
        ↓
Resume Parsing
        ↓
Skill Extraction
        ↓
Role Prediction
        ↓
Question Generation
        ↓
Context Retrieval
        ↓
Interview Question
        ↓
Candidate Answer Submission
        ↓
Answer Evaluation
        ↓
Report Generation
        ↓
Final Interview Report
```

---

# Detailed Workflow

## Step 1 — Resume Upload

The candidate uploads a PDF resume using the Streamlit interface.

Input:

```text
Resume.pdf
```

---

## Step 2 — Resume Parsing

The Resume Parser:

* Extracts text from PDF.
* Cleans text.
* Removes unnecessary symbols.

Output:

```text
Clean Resume Text
```

---

## Step 3 — Skill Extraction

Technical skills are extracted from resume text.

Examples:

* Python
* SQL
* Spark
* Kafka
* Machine Learning

Output:

```text
Extracted Skills
```

---

## Step 4 — Role Prediction

The ML model predicts the candidate's target role.

Examples:

```text
Python Developer
Data Engineer
ML Engineer
Data Analyst
```

---

## Step 5 — Question Generation

The Question Generation Agent:

* Uses predicted role.
* Retrieves relevant knowledge.
* Generates interview questions.

Output:

```text
Interview Question
Expected Answer
```

---

## Step 6 — Candidate Answer Submission

The candidate enters an answer through the Streamlit UI.

Output:

```text
Candidate Answer
```

---

## Step 7 — Answer Evaluation

The Answer Evaluation Agent:

* Compares expected and candidate answers.
* Computes similarity score.
* Generates feedback.

Output:

```text
Score + Feedback
```

---

## Step 8 — Final Report Generation

The Report Generator prepares:

* Total Questions
* Average Score
* Individual Feedback
* Detailed Interview Summary

Output:

```text
Final Interview Report
```

---

# Workflow Summary

```text
Resume
   ↓
Parsing
   ↓
Skills
   ↓
Role Prediction
   ↓
Question Generation
   ↓
Answer Submission
   ↓
Evaluation
   ↓
Final Report
```
