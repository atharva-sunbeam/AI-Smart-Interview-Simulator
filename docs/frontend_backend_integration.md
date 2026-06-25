# Frontend Backend Integration

## Architecture

Streamlit UI
↓
SystemController
↓
Backend Modules

---

## Purpose

The frontend should never directly call backend modules.

Instead, all communication passes through the SystemController.

This architecture improves:

* Maintainability
* Modularity
* Scalability
* Testability

---

## Workflow

Resume Upload
↓
SystemController.run_complete_pipeline()
↓
Resume Parsing
↓
Skill Extraction
↓
Role Prediction
↓
Start Interview
↓
Question Generation
↓
Answer Evaluation
↓
Report Generation

---

## Benefits

### Loose Coupling

Frontend remains independent from backend implementation details.

### Centralized Control

SystemController orchestrates the complete system.

### Production Ready Design

Modern enterprise systems commonly use a controller/service layer between UI and business logic.
