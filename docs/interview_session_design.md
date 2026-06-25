# Interview Session Design

## Purpose

The Interview Session module orchestrates the complete AI interview workflow.

It acts as the central coordinator between all agents.

---

# Architecture

Resume PDF

↓

Resume Parser

↓

Skill Extraction

↓

Role Prediction

↓

Question Generation Agent

↓

Interview Question

↓

Candidate Answer

↓

Answer Evaluation Agent

↓

Score + Feedback

↓

Final Interview Report

---

# Responsibilities

The Interview Session module performs:

* Session initialization
* Question generation
* Answer submission
* Answer evaluation
* Report generation

---

# Core Functions

## start_session()

Initializes a new interview session.

Input:

Predicted Role

Example:

Python Developer

---

## ask_question()

Requests a question from the Question Generation Agent.

Output:

Technical interview question

---

## submit_answer()

Stores candidate responses.

Input:

Candidate answer text

---

## evaluate_answer()

Evaluates candidate responses.

Current Version:

Placeholder evaluation

Future Version:

ML-based Answer Evaluation Agent

---

## generate_report()

Produces final interview summary.

Example:

* Total Questions
* Average Score
* Detailed Feedback

---

# Benefits

* Centralized orchestration
* Modular architecture
* Easy future expansion
* Supports multi-agent workflows

---

# Future Enhancements

Phase 1:

Single-question interviews

Phase 2:

Multi-question interviews

Phase 3:

Adaptive interviews

Phase 4:

Real-time conversational interviews

---

# Final Architecture

Interview Session

↓

Question Agent

↓

Answer Evaluation Agent

↓

Final Report
