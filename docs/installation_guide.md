# Installation Guide

## AI Smart Interview Simulator

---

# 1. Clone the Repository

```bash
git clone https://github.com/atharva-sunbeam/AI-Smart-Interview-Simulator.git

cd AI-Smart-Interview-Simulator
```

---

# 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

# 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 4. Train the Role Prediction Model

```bash
python ml_models/role_prediction/train_role_classifier.py
```

This generates the trained Logistic Regression model used for role prediction.

---

# 5. Generate Embeddings

Run the embedding generation pipeline after preparing the knowledge base.

Example:

```bash
python embedding_pipeline/generate_embeddings.py
```

---

# 6. Index Documents into ChromaDB

Populate the vector database.

Example:

```bash
python vector_db/index_documents.py
```

---

# 7. Run Streamlit

```bash
streamlit run frontend/app.py
```

---

# 8. Run the Demo

```bash
python scripts/demo_run.py
```

---

# 9. Execute Unit Tests

Run all tests:

```bash
pytest
```

Run an individual test:

```bash
pytest tests/test_answer_evaluation_agent.py -v
```

---

# Project Workflow

Resume Upload

↓

Resume Parsing

↓

Role Prediction (ML)

↓

Question Generation (RAG)

↓

Interview Session

↓

Answer Evaluation (ML)

↓

Report Generation

↓

JSON Report

---

# Troubleshooting

## Missing Packages

```bash
pip install -r requirements.txt
```

## ChromaDB Errors

Delete the local database and recreate it.

## Missing ML Model

Train the classifier again using:

```bash
python ml_models/role_prediction/train_role_classifier.py
```

---

# Technologies

* Python
* Streamlit
* Scikit-learn
* ChromaDB
* LangChain
* Sentence Transformers
* PyPDF2
* Ollama
* Joblib
* Pytest
