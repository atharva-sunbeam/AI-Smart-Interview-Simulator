# 🤖 AI-Powered Smart Technical Interview Simulator

An enterprise-grade, multi-agent technical interview simulation platform powered by **Retrieval-Augmented Generation (RAG)**, **Groq Cloud API (`llama-3.3-70b-versatile`)**, **ChromaDB Vector Store**, and **Streamlit**.

---

### 🌐 Live Application Link
- **Production HTTPS URL:** [https://ai-interview-sim.duckdns.org](https://ai-interview-sim.duckdns.org)
- **AWS Elastic IP:** `http://43.205.63.85`

---

## 📌 Domain
**Artificial Intelligence / Generative AI / EdTech & Automated Assessment Systems**

---

## 🎯 Problem Statement
Traditional technical mock interview tools and static question banks are generic, lack domain specificity, and fail to simulate real-world technical grilling. Candidates struggle to get personalized, role-aligned feedback based on their actual resume projects, exact tech stack, and difficulty requirements. Furthermore, human mock interviews are expensive, non-scalable, and inconsistent in evaluation metrics.

---

## 🚀 Objective
To engineer an autonomous, scalable, multi-agent AI interview platform that:
1. **Parses candidate resumes** to extract exact technical skills, domain expertise, tools, and project descriptions without false positives.
2. **Predicts and matches target engineering roles** across 50+ specialized disciplines (Data/AI, Cloud/DevOps, Software/Systems, Cyber Security).
3. **Retrieves domain-specific technical knowledge** via a high-performance RAG pipeline using ChromaDB vector database.
4. **Enforces strict difficulty controls** (Easy, Medium, Hard) to ensure question complexity never drifts.
5. **Provides hands-free voice-based interviewing** with real-time speech-to-text transcription (STT) and auto-spoken audio playback (TTS) over HTTPS.
6. **Generates diagnostic scorecards** and performance evaluation reports with continuous RAG vector store learning.

---

## 🛠️ Tech Stack

| Domain | Technologies & Libraries |
| :--- | :--- |
| **LLM Engine & Multi-Agent** | Groq Cloud API (`llama-3.3-70b-versatile`), LangChain, CrewAI, Ollama (Local Fallback) |
| **RAG & Vector Database** | ChromaDB, HuggingFace Sentence-Transformers (`all-MiniLM-L6-v2`), LangChain VectorStore |
| **User Interface & Audio** | Streamlit, Web Speech API (Bi-Directional Voice TTS & STT over Secure HTTPS) |
| **Data Scraping & Processing** | Python 3.12, BeautifulSoup4, PyPDF2, Pandas, Requests |
| **Cloud Infrastructure & Security** | AWS EC2 (`c7i-flex.large`), Elastic IP, Nginx Reverse Proxy, Let's Encrypt SSL (Certbot), Systemd, Ubuntu 24.04 LTS |

---

## Key Features

- 📄 **Precise Skill & Project Parsing**: Analyzes uploaded PDF resumes using strict regex word boundaries (`(?:\b|_)`) and LLM extraction to isolate exact tech stacks without false positive skill leakage.
- 🎯 **50+ Engineering Role Support**: Auto-predicts target roles and supports specialized blueprints across Software, Cloud, DevOps, Machine Learning, Data Engineering, and Security.
- 🔒 **Strict Fixed Difficulty Lock**: Enforces exact difficulty tiers (Easy: Definitions/Basics, Medium: Practical/Scenarios, Hard: System Design/Architecture) without dynamic difficulty drift.
- 🧠 **RAG-Powered Context Retrieval**: Queries ChromaDB vector database for verified domain knowledge, preventing LLM hallucinations.
- 🔄 **Cross-Session Question Non-Repetition**: Tracks asked questions globally to guarantee zero repeated questions across sessions.
- 🎙️ **Bi-Directional Voice Interface**: Hands-free speech recognition (STT) into text areas and native auto-spoken audio (TTS) question playback under HTTPS secure context.
- 📊 **Independent Follow-Up Question Evaluation**: Evaluates main and follow-up responses independently, generating diagnostic performance scorecards.
- 🚀 **Continuous RAG Learning**: Automatically feeds evaluated candidate Q&A pairs back into the ChromaDB vector database to continuously expand the knowledge base.

---

## 🏛️ System Architecture Overview

```mermaid
graph TD
    User([Candidate / User]) -->|1. Upload PDF Resume| ResumeAgent[Resume Analysis Agent]
    ResumeAgent -->|Extracts Skills, Tools & Projects| RoleCatalog[Role & Skill Predictor]
    RoleCatalog -->|Suggests Target Role| QGen[Question Synthesis Agent]
    
    User -->|2. Configures Role & Fixed Difficulty| QGen
    QGen -->|3. Queries Context| RAG[RAG Retrieval Pipeline]
    RAG -->|Vector Search| ChromaDB[(ChromaDB Vector Store)]
    ChromaDB -->|Relevant Context & Blueprints| QGen
    
    QGen -->|4. Synthesizes Blueprint Question| AudioTTS[Web Speech TTS Audio]
    AudioTTS -->|5. Speaks Question & Renders UI| User
    
    User -->|6. Record Voice / Type Answer| VoiceSTT[Voice Speech-to-Text]
    VoiceSTT -->|Transcribes Answer| EvalAgent[Answer Evaluator Agent]
    EvalAgent -->|7. Scores & Diagnoses Answer| FollowUp[Follow-Up Question Agent]
    
    FollowUp -->|8. Generates Standalone Follow-Up| User
    EvalAgent -->|9. Continuous RAG Learning| ChromaDB
    EvalAgent -->|10. Final Scorecard & Feedback Report| Feedback[Feedback & Report Generator]
    Feedback -->|Detailed Assessment PDF/JSON| User
```

---

## 📂 Dataset & Input Sources

1. **Scraped Technical Blueprints**: Technical interview questions scraped and cleaned across 50+ engineering domains (`datasets/raw/` & `datasets/cleaned/`).
2. **Unified Knowledge Base**: Processed CSV knowledge base (`datasets/processed/unified_knowledge_base.csv`) compiled into ChromaDB vector embeddings.
3. **Candidate Resumes**: User-uploaded PDF technical resumes parsed at runtime.

---

## 💻 Installation and Execution

### Local Setup (Windows / Linux / macOS)

1. **Clone the Repository**:
   ```bash
   git clone -b dev https://github.com/atharva-sunbeam/AI-Smart-Interview-Simulator.git
   cd AI-Smart-Interview-Simulator
   ```

2. **Create & Activate Virtual Environment**:
   - **Windows (PowerShell):**
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - **Linux / macOS:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Seed Knowledge Base Vector Store**:
   ```bash
   python -m scraper.seed_knowledge
   ```

6. **Run Streamlit Web Application**:
   ```bash
   streamlit run app.py
   ```
   Open `http://localhost:8501` in your browser.

---

### Cloud Deployment Setup (AWS EC2 + HTTPS SSL)

1. **Launch EC2 Instance & Attach Elastic IP**:
   - **AMI:** Ubuntu Server 24.04 LTS (x86_64)
   - **Instance Type:** `c7i-flex.large` (2 vCPU, 4 GB RAM, 25 GB GP3 SSD)
   - **Security Group Inbound Rules:**
     - SSH (Port 22) -> Anywhere (`0.0.0.0/0`)
     - HTTP (Port 80) -> Anywhere (`0.0.0.0/0`)
     - HTTPS (Port 443) -> Anywhere (`0.0.0.0/0`)
     - Custom TCP (Port 8501) -> Anywhere (`0.0.0.0/0`)
   - **Elastic IP:** Attach a static Elastic IP (e.g. `43.205.63.85`).

2. **Connect & Setup Environment**:
   ```bash
   ssh -i "ai-interview-key.pem" ubuntu@<YOUR-ELASTIC-IP>
   sudo apt update && sudo apt upgrade -y
   sudo apt install -y python3-pip python3-venv git nginx systemd certbot python3-certbot-nginx
   
   git clone -b dev https://github.com/atharva-sunbeam/AI-Smart-Interview-Simulator.git ai-interview
   cd ai-interview
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure Systemd Background Service (`/etc/systemd/system/ai-interview.service`)**:
   ```ini
   [Unit]
   Description=AI Smart Technical Interview Simulator Streamlit App
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/ai-interview
   ExecStart=/home/ubuntu/ai-interview/venv/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0
   Restart=always
   RestartSec=5
   Environment="PATH=/home/ubuntu/ai-interview/venv/bin:/usr/bin"

   [Install]
   WantedBy=multi-user.target
   ```
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable ai-interview
   sudo systemctl start ai-interview
   ```

4. **Nginx Reverse Proxy & Certbot Free SSL**:
   ```bash
   sudo nano /etc/nginx/sites-available/default
   ```
   ```nginx
   server {
       listen 80;
       server_name ai-interview-sim.duckdns.org;

       location / {
           proxy_pass http://127.0.0.1:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
       }
   }
   ```
   ```bash
   sudo systemctl reload nginx
   sudo certbot --nginx -d ai-interview-sim.duckdns.org
   ```

---

## 🔄 End-to-End Workflow

```
[Resume Upload] -> [Skill & Project Extraction] -> [Role Prediction & Parameter Selection]
                                                               ↓
                                               [RAG Vector Knowledge Query]
                                                               ↓
                                             [Topic Blueprint Question Synthesis]
                                                               ↓
                                         [Voice Playback & Hands-Free Recording]
                                                               ↓
                                             [Independent Technical Evaluation]
                                                               ↓
                                              [Follow-Up Question Handling]
                                                               ↓
                                       [Diagnostic Scorecard & Continuous Learning]
```

---

## 🔮 Future Enhancements

- 🌐 **Multi-Lingual Interview Support**: Add support for non-English technical mock interviews.
- 💻 **Interactive Coding Sandbox**: Integrate an online code editor (Monaco/Ace) with automated unit test execution.
- 📹 **Multimodal Emotion & Confidence Analysis**: Facial posture and tone analysis during video mock interviews.
- 🏢 **Enterprise Recruiter Analytics Dashboard**: Centralized applicant scoring and talent match dashboards for hiring managers.

---

## 👥 Authors & Contact Information

- **Shreyas Deshingkar** — Email: [shreyasdeshingkar@gmail.com](mailto:shreyasdeshingkar@gmail.com)
- **Atharva Birje** — Email: [atharvapersonal234@gmail.com](mailto:atharvapersonal234@gmail.com)

---

## 📌 Conclusion
The **AI-Powered Smart Technical Interview Simulator** bridges the gap between static preparation resources and dynamic technical evaluations. By combining Multi-Agent LLMs with Retrieval-Augmented Generation, strict difficulty controls, bi-directional voice interfaces over HTTPS, and continuous RAG database learning, it delivers a realistic, scalable, and highly accurate mock interview platform for modern software engineering candidates.
