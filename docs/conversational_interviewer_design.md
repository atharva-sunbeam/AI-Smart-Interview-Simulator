# Conversational Interviewer Design

## Purpose

The Conversational Interviewer Agent introduces intelligent interview flow management into the AI Smart Interview Simulator.

Instead of asking unrelated static questions, the system dynamically decides whether to:

* Ask a follow-up question
* Move to a new topic
* End the interview

---

## Architecture

Candidate Answer
↓
Answer Evaluation
↓
ConversationalInterviewerAgent
↓
Decision Engine
↓

FOLLOW_UP
NEXT_TOPIC
END_INTERVIEW

---

## Components

### start_interview()

Initializes interview state.

Stores:

* Candidate role
* Interview history
* Follow-up depth

---

### generate_initial_question()

Generates the first interview question using the QuestionGenerationAgent.

---

### generate_followup_question()

Creates deeper technical questions based on:

* Previous question
* Candidate answer
* Interview history

Example:

Question:
Explain decorators.

Follow-up:
Can decorators accept parameters?

---

### decide_next_action()

Decision rules:

* Score < 40 → FOLLOW_UP
* Score > 80 → NEXT_TOPIC
* Follow-up depth >= 2 → NEXT_TOPIC

---

## Benefits

* Produces conversational interviews
* Simulates real interviewer behavior
* Enables adaptive interviews
* Improves candidate assessment quality

---

## Future Improvements

Future versions will integrate:

* Ollama + Mistral
* LLM-based follow-up generation
* Adaptive difficulty adjustment
* Conversational memory

---

## Limitations

Current implementation uses rule-based follow-up generation.

Future versions will replace this with LLM-driven question generation.
