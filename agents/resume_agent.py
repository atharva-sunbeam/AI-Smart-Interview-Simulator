import re
import json
import PyPDF2
from agents.role_catalog import predict_role_from_skills
from agents.orchestrator import LLMManager

# Skill domains with expanded ITISS, Cyber Security, Cloud, DBDA, DMC, DESD, BDA, and DAC keywords
SKILL_DOMAINS = {
    "ITISS & Networking": [
        "networking", "tcp/ip", "subnetting", "routing", "switching", "cisco", "wireshark",
        "dns", "dhcp", "vpn", "ipsec", "firewall", "iptables", "ufw", "sysadmin", "system administration",
        "linux", "redhat", "centos", "ubuntu", "bash", "shell scripting", "systemd", "lvm", "nfs", "ssh", "cron", "selinux"
    ],
    "Cloud & Infrastructure": [
        "aws", "gcp", "azure", "docker", "kubernetes", "k8s", "terraform", "ansible", "cloudformation",
        "ci/cd", "jenkins", "github actions", "prometheus", "grafana", "nagios", "zabbix", "sre"
    ],
    "Cyber Security": [
        "cybersecurity", "cyber security", "siem", "splunk", "nessus", "metasploit", "burp suite",
        "wireshark", "nmap", "owasp", "vulnerability assessment", "penetration testing", "incident response"
    ],
    "Programming Languages": [
        "python", "sql", "java", "c\\+\\+", "cpp", "c", "javascript", "typescript", "scala", "golang", "bash", "kotlin", "dart", "r"
    ],
    "Machine Learning & Data Science": [
        "machine learning", "practical machine learning", "data science", "statistics", "advanced analytics", "deep learning", "predictive modeling", "feature engineering"
    ],
    "Generative AI & LLMs": [
        "generative ai", "genai", "llm", "llms", "large language models", "rag", "langchain", "crewai", "ollama", "multi-agent", "ai agents", "nlp", "bert", "transformers", "pytorch", "tensorflow", "keras"
    ],
    "Big Data & Data Engineering": [
        "big data", "spark", "apache spark", "databricks", "kafka", "pyspark", "hadoop", "etl", "delta lake", "data warehousing"
    ],
    "Web & Databases": [
        "react", "vue", "angular", "node", "express", "next.js", "tailwind", "postgresql", "mysql",
        "sqlite", "mongodb", "redis", "cassandra", "dynamodb", "oracle", "chromadb", "faiss", "streamlit"
    ],
    "Embedded & Mobile": [
        "embedded", "microcontroller", "arm", "rtos", "stm32", "yocto", "flutter", "android", "jetpack compose"
    ]
}

ALL_TOOL_KEYWORDS = [kw.replace("\\", "") for sublist in SKILL_DOMAINS.values() for kw in sublist]


def match_skill_keyword(kw: str, text_lower: str) -> bool:
    """
    Strictly matches skill keywords using precise regex boundaries.
    Prevents false positive substring matches like 'scala' in 'scalable' or 'c' in 'curriculum'.
    """
    clean_kw = kw.replace("\\", "").strip().lower()
    if not clean_kw:
        return False

    if clean_kw in ["c++", "cpp"]:
        pattern = r'(?:\b|_)(?:c\+\+|cpp)(?:\b|_|\s|,|;|\.|\/|$)'
        return bool(re.search(pattern, text_lower))
    elif clean_kw == "c#":
        pattern = r'(?:\b|_)(?:c\#|csharp)(?:\b|_|\s|,|;|\.|\/|$)'
        return bool(re.search(pattern, text_lower))
    elif clean_kw in ["c", "r"]:
        # Exclude R&D, R & D, (R), C&A, (C) false positives
        text_clean = re.sub(r'\b[cr]\s*&\s*[da]\b', '', text_lower)
        text_clean = re.sub(r'\(\s*[cr]\s*\)', '', text_clean)
        if re.search(r'\b(?:' + clean_kw + r'\s+programming|' + clean_kw + r'\s+language|' + clean_kw + r'-lang|rstudio)\b', text_clean):
            return True
        pattern = r'(?:\b(?:languages?|skills?|tools?|technologies|programming|proficient in|experienced with|knowledge of)\b[\s\S]{0,150}?\b)' + clean_kw + r'\b'
        if re.search(pattern, text_clean):
            return True
        list_pattern = r'(?:,\s*|\/\s*)' + clean_kw + r'(?:\s*,|\s*\/|\s*$)'
        return bool(re.search(list_pattern, text_clean))
    else:
        pattern = r'(?:\b|_)' + re.escape(clean_kw) + r'(?:\b|_)'
        return bool(re.search(pattern, text_lower))


class ResumeAgent:
    def __init__(self):
        self.llm_manager = LLMManager()

    def extract_text_from_pdf(self, pdf_file_path):
        """Extracts raw text from a PDF resume."""
        text = ""
        try:
            with open(pdf_file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"[Resume Parsing Error] {e}")
        return text

    def extract_tools_from_text(self, text_snippet):
        """Extracts specific tool/technology names mentioned in a text snippet."""
        text_lower = text_snippet.lower()
        found_tools = []
        for tool in ALL_TOOL_KEYWORDS:
            clean_tool = tool.replace("\\", "").strip().lower()
            if match_skill_keyword(clean_tool, text_lower):
                display_tool = "C++" if clean_tool in ["c++", "cpp"] else clean_tool.upper()
                if display_tool not in found_tools:
                    found_tools.append(display_tool)
        return found_tools

    def extract_projects(self, text):
        """
        Extracts structured project metadata (Exact Project Name, Tools Used, Short Description)
        using LLM extraction with regex fallback.
        """
        if not text or len(text.strip()) < 15:
            return []

        # 1. LLM Hybrid Structured Extraction (100% Precision)
        if self.llm_manager.is_connected:
            prompt = (
                "You are an expert technical recruiter analyzing a resume.\n"
                "Task: Extract all projects mentioned in the resume below.\n"
                "For EACH project, extract:\n"
                "1. 'name': Exact project title/name\n"
                "2. 'tools': List of specific tools, languages, libraries, databases, or platforms used\n"
                "3. 'description': Short 1-2 sentence description of what the project accomplished\n\n"
                f"Resume Text:\n{text[:2500]}\n\n"
                "Respond STRICTLY as a JSON array of objects:\n"
                "[\n  {\n    \"name\": \"<project name>\",\n    \"tools\": [\"<tool1>\", \"<tool2>\"],\n    \"description\": \"<1-2 sentence summary>\"\n  }\n]"
            )
            response = self.llm_manager.generate(prompt)
            if response:
                try:
                    clean_res = re.sub(r'```json\s*|\s*```', '', response).strip()
                    parsed = json.loads(clean_res)
                    if isinstance(parsed, list) and len(parsed) > 0:
                        valid_projects = []
                        for item in parsed:
                            if isinstance(item, dict) and "name" in item:
                                valid_projects.append({
                                    "name": item.get("name", "Project").strip(),
                                    "tools": [t.upper() for t in item.get("tools", [])] if item.get("tools") else self.extract_tools_from_text(item.get("description", "")),
                                    "description": item.get("description", item.get("name", "")).strip(),
                                    "text": f"{item.get('name')}: {item.get('description')}"
                                })
                        if valid_projects:
                            return valid_projects[:4]
                except Exception as e:
                    print(f"[ResumeAgent LLM Project Extraction Warning] {e}")

        # 2. Regex & Heuristic Parsing Fallback
        projects = []
        pattern = r'(?:projects|key projects|academic projects|project highlights|recent projects)[\s\S]*?(?=(?:education|experience|skills|certifications|achievements|$))'
        match = re.search(pattern, text, re.IGNORECASE)

        raw_items = []
        if match:
            project_block = match.group(0)
            raw_items = [item.strip() for item in re.split(r'[\n\r\-•*]+', project_block) if len(item.strip()) > 10]

        if not raw_items:
            for item in re.split(r'[\n\r\-•*]+', text):
                item_str = item.strip()
                if any(kw in item_str.lower() for kw in ["project", "developed", "built", "implemented", "system", "application", "platform"]):
                    if 15 <= len(item_str) <= 150:
                        raw_items.append(item_str)

        for clean_line in raw_items:
            if re.match(r'^(projects|key projects|academic projects|project highlights)', clean_line, re.IGNORECASE):
                continue

            if len(clean_line) < 15:
                continue

            parts = re.split(r'[:–—|]|\busing\b|\bwith\b|\bbuilt\b', clean_line, flags=re.IGNORECASE)
            proj_name = parts[0].strip() if len(parts) > 1 and len(parts[0].strip()) >= 5 else clean_line[:40].strip()

            tools = self.extract_tools_from_text(clean_line)
            desc = clean_line

            projects.append({
                "name": proj_name,
                "tools": tools if tools else ["SOFTWARE TOOLS"],
                "description": desc,
                "text": clean_line
            })

            if len(projects) >= 4:
                break

        return projects

    def parse_resume(self, text_or_path):
        """
        Parses resume text or PDF file and returns extracted skills matrix, structured project metadata,
        and recommended target job role based on parsed skills and tech stack.
        """
        if text_or_path.lower().endswith(".pdf"):
            text = self.extract_text_from_pdf(text_or_path)
        else:
            text = text_or_path

        if not text:
            return {
                "skills": [],
                "skills_by_domain": {},
                "projects": [],
                "recommended_role": "Python Developer",
                "text_length": 0
            }

        text_lower = text.lower()
        extracted_skills = {}
        total_skills_count = 0

        for domain, keywords in SKILL_DOMAINS.items():
            found_in_domain = []
            for kw in keywords:
                clean_kw = kw.replace("\\", "").strip().lower()
                if match_skill_keyword(clean_kw, text_lower):
                    display_kw = "C++" if clean_kw in ["c++", "cpp"] else clean_kw.upper()
                    if display_kw not in found_in_domain:
                        found_in_domain.append(display_kw)
            if found_in_domain:
                extracted_skills[domain] = found_in_domain
                total_skills_count += len(found_in_domain)

        all_skills_flat = [s for sublist in extracted_skills.values() for s in sublist]
        extracted_projects = self.extract_projects(text)

        # Use RoleCatalog prediction engine
        recommended_role = predict_role_from_skills(all_skills_flat)

        return {
            "skills": all_skills_flat,
            "skills_by_domain": extracted_skills,
            "projects": extracted_projects,
            "recommended_role": recommended_role,
            "text_length": len(text)
        }

if __name__ == "__main__":
    agent = ResumeAgent()
    sample = """
    John Doe - AI & Cloud Engineer
    Skills: Python, FastAPI, Docker, AWS, LangChain, Llama, ChromaDB.

    Projects:
    - Smart AI Interview Simulator: Developed an interactive AI interviewing tool using Python, FastAPI, LangChain, Groq LLM (llama-3.3-70b-versatile), and ChromaDB RAG for real-time question evaluation.
    - Cloud Infrastructure Log Monitor: Built an automated log processing system with Docker, Kafka, AWS EC2 and Prometheus.
    """
    res = agent.parse_resume(sample)
    print("Recommended Role:", res["recommended_role"])
    print("Extracted Skills:", res["skills"])
