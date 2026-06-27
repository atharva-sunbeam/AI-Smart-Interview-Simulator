# System Testing Strategy

## Purpose

Ensure the AI Smart Interview Simulator functions reliably across all modules.

---

# Testing Levels

## 1. Unit Testing

Individual modules are tested independently.

Examples:

* Resume Parser
* Role Classifier
* Retriever
* Question Agent
* Answer Evaluation Agent

Tool:

pytest

---

## 2. Integration Testing

Multiple modules are tested together.

Example:

Resume Parser
↓
Role Prediction
↓
Question Generation

Purpose:

Validate communication between components.

---

## 3. End-to-End Testing

Validate the complete system workflow.

Pipeline:

Resume Upload
↓
Resume Parsing
↓
Role Prediction
↓
Question Generation
↓
Answer Submission
↓
Answer Evaluation
↓
Report Generation

---

# Exception Handling Tests

The system should gracefully handle:

* Missing resume file
* Empty resume
* Missing ML model
* Missing embeddings
* Retriever failure
* ChromaDB unavailable
* Empty candidate answer

Fallback mechanisms should always prevent application crashes.

---

# Expected Result

The system should continue operating even if individual modules fail.

Fallback defaults:

* Default role → Python Developer
* Default question → Explain decorators in Python.
* Default evaluation → Score = 0

---

# Testing Framework

Framework:

pytest

Coverage Goal:

80%+

Future:

CI/CD integration using GitHub Actions.
