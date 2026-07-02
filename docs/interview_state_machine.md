# Interview State Machine

## Overview

The Interview State Machine is responsible for controlling the complete
interview lifecycle in the AI Smart Interview Simulator.

Instead of allowing interview components to operate independently,
the state machine ensures that every interview follows a structured,
predictable workflow.

This design improves:

- Reliability
- Maintainability
- Future extensibility
- Conversational flow

---

# Purpose

The Interview State Machine provides a centralized controller that keeps
track of the current interview state, interview context, and transitions
between different phases of the interview.

It prevents invalid transitions such as:

- Evaluating before receiving an answer
- Asking follow-up questions before evaluation
- Ending an interview without generating a summary

---

# Interview Flow

```

START
│
▼
INTRODUCTION
│
▼
QUESTION
│
▼
LISTENING
│
▼
THINKING
│
├───────────────┐
│               │
▼               ▼
FOLLOWUP     NEXT_TOPIC
│               │
└───────┬───────┘
│
▼
SUMMARY
│
▼
END

```

---

# State Descriptions

## START

Initial state.

Responsibilities:

- Initialize interview
- Create interview context
- Reset previous session

---

## INTRODUCTION

Responsibilities:

- Welcome candidate
- Display interview instructions
- Prepare interview session

---

## QUESTION

Responsibilities:

- Generate technical interview question
- Store current question
- Update interview context

---

## LISTENING

Responsibilities:

- Wait for candidate response
- Record audio (future)
- Accept text input
- Generate transcript

---

## THINKING

Responsibilities:

- Evaluate candidate answer
- Compute similarity score
- Determine interview quality
- Decide next interview action

---

## FOLLOWUP

Responsibilities:

- Generate follow-up question
- Increase follow-up counter
- Continue same topic

---

## NEXT_TOPIC

Responsibilities:

- Select new technical topic
- Adjust interview difficulty
- Generate new interview question

---

## SUMMARY

Responsibilities:

- Compute interview statistics
- Prepare candidate summary
- Generate recommendations

---

## END

Responsibilities:

- Save interview report
- Record interview duration
- Close interview session

---

# Interview Context

The Interview Context stores all information required
throughout the interview.

Fields:

| Field | Description |
|--------|-------------|
| current_topic | Active interview topic |
| current_question | Current interview question |
| previous_question | Previously asked question |
| previous_answer | Previous candidate answer |
| difficulty | Current interview difficulty |
| candidate_score | Latest evaluation score |
| confidence_score | Reserved for future confidence estimation |
| followup_count | Number of follow-up questions |
| interview_duration | Total interview duration |
| conversation_history | Complete interview history |
| start_time | Interview start timestamp |

---

# Transition Rules

| Current State | Next State |
|---------------|------------|
| START | INTRODUCTION |
| INTRODUCTION | QUESTION |
| QUESTION | LISTENING |
| LISTENING | THINKING |
| THINKING | FOLLOWUP |
| THINKING | NEXT_TOPIC |
| FOLLOWUP | LISTENING |
| NEXT_TOPIC | QUESTION |
| QUESTION | SUMMARY |
| SUMMARY | END |

---

# Interview Flow Agent

The Interview Flow Agent works together with the
Interview State Machine.

Responsibilities:

- Decide whether a follow-up question is required
- Decide whether to change interview topic
- Recommend interview difficulty
- Decide when to end interview

The Flow Agent does **not** modify interview data.
It only analyzes the current interview context and
returns the recommended next action.

---

# Integration Architecture

```

                Streamlit UI
│
▼
Interview Session
│
▼
Interview State Machine
│
▼
Interview Flow Agent
│
├─────────────┐
│             │
▼             ▼
Question      Evaluation
Generation      Agent
│             │
└──────┬──────┘
│
▼
Text-to-Speech
│
▼
Candidate
│
▼
Speech-to-Text
│
▼
Evaluation
│
▼
State Machine

```

---

# Current Features

Implemented:

- Finite-state machine
- Interview context management
- State transitions
- Conversation history
- Difficulty tracking
- Candidate score tracking
- Follow-up tracking
- Interview duration tracking

---

# Planned Enhancements

Future versions will include:

- Live microphone streaming
- Real-time transcription
- Dynamic follow-up generation
- Adaptive interview difficulty
- Confidence estimation
- Candidate emotion analysis
- Eye-contact detection
- Gesture recognition
- Real-time interviewer memory
- Multi-round interview support

---

# Benefits

The Interview State Machine provides:

- Structured interview workflow
- Clear separation of responsibilities
- Easier debugging
- Improved scalability
- Production-ready architecture
- Future conversational interview support

---

# Testing

Unit tests validate:

- Initial state
- State transitions
- Follow-up transitions
- Topic transitions
- Summary state
- End state
- Reset functionality

Run tests:

```bash
python -m pytest tests/test_interview_state_machine.py -v
```

Expected Result:

```
10 passed
```

---

# Future Integration

The Interview State Machine will be integrated into:

```
backend/interview_session.py
```

during the **feature-live-interview-engine** sprint.

The interview loop will become:

```
AI Generates Question
        │
        ▼
Text-to-Speech
        │
        ▼
Candidate Speaks
        │
        ▼
Speech-to-Text
        │
        ▼
Answer Evaluation
        │
        ▼
Interview State Machine
        │
        ▼
Interview Flow Agent
        │
        ▼
Next Question / Follow-up
```

This architecture enables a continuous, natural,
AI-driven interview experience.