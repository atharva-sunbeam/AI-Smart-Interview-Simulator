# Ollama Interview Brain

## Overview

The Ollama Interview Brain enables the AI Smart Interview Simulator
to generate dynamic interview questions, intelligent follow-up questions,
evaluate conceptual depth, and summarize interview progress using a
locally hosted Large Language Model (LLM).

This replaces static interview questions with conversational,
context-aware interviewing.

---

# Architecture

```
                Streamlit UI
                      │
                      ▼
             Interview Session
                      │
                      ▼
        Question Generation Agent
                      │
                      ▼
         Ollama Interview Agent
                      │
                      ▼
              Ollama Server
                      │
                      ▼
            Mistral 7B Instruct
```

---

# Components

## OllamaInterviewAgent

Responsibilities:

- Generate interview questions
- Generate follow-up questions
- Evaluate answer depth
- Summarize interview progress

---

## Prompt Configuration

All prompt templates are stored inside:

```
config/interview_prompts.py
```

Benefits:

- Cleaner code
- Easier prompt tuning
- Reusable prompts
- Future model compatibility

---

# Model

Current Model:

```
mistral:7b-instruct
```

Future Supported Models:

- Llama 3
- DeepSeek
- Gemma
- Phi
- OpenAI GPT

---

# Interview Workflow

```
Role Prediction
        │
        ▼
Question Generation
        │
        ▼
Candidate Answer
        │
        ▼
Depth Evaluation
        │
        ▼
Follow-up Question
        │
        ▼
Interview Summary
```

---

# Question Generation

Inputs:

- Candidate Role
- Interview Topic

Output:

One technical interview question.

Example:

```
Role:
Python Developer

Topic:
Decorators

Output:

Explain Python decorators with a practical example.
```

---

# Follow-up Question Generation

Inputs:

- Candidate Role
- Topic
- Previous Question
- Candidate Answer

Output:

One deeper follow-up question.

Example:

Previous Question:

Explain decorators.

Candidate Answer:

Decorators modify functions.

Follow-up:

Can decorators accept arguments? Explain with an example.

---

# Depth Evaluation

The LLM evaluates:

- Technical correctness
- Conceptual understanding
- Completeness
- Communication quality

Example Output:

```
Depth Score: 82

The candidate demonstrates a good understanding
of decorators but does not explain wrapper
functions or practical implementation.
```

---

# Interview Summary

At the end of the interview the model generates:

- Strengths
- Weaknesses
- Topics covered
- Overall assessment

Example:

```
Strengths

- Good Python fundamentals
- Clear communication

Weaknesses

- Limited system design knowledge

Overall

Candidate demonstrates solid backend
development skills.
```

---

# Advantages

Compared with static questions:

✔ Dynamic interviewing

✔ Adaptive follow-up questions

✔ Better realism

✔ More natural conversations

✔ Interview memory

---

# Error Handling

The Ollama Interview Agent handles:

- Ollama server unavailable
- Model not installed
- Empty responses
- Network/API failures

The application continues running and returns
a descriptive error message instead of crashing.

---

# Future Improvements

- Multi-turn conversational memory
- Difficulty adaptation
- Company-specific interview styles
- Coding interview generation
- Behavioral interview generation
- Voice-enabled interviewer
- Real-time confidence estimation
- Multi-model support

---

# Technologies Used

- Python
- Ollama
- Mistral 7B Instruct
- Prompt Engineering
- Streamlit
- Modular Agent Architecture