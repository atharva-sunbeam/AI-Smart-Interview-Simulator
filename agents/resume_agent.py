import re
import PyPDF2

# Predefined skill keywords for pattern matching
SKILL_DOMAINS = {
    "Languages": ["python", "sql", "java", "c\\+\\+", "javascript", "typescript", "scala", "golang", "r", "bash", "html", "css"],
    "Python Frameworks": ["django", "flask", "fastapi", "numpy", "pandas", "scipy", "celery", "poetry", "streamlit"],
    "Frontend & Web": ["react", "vue", "angular", "node", "express", "next.js", "tailwind", "bootstrap", "html5", "css3"],
    "Data Engineering": ["spark", "pyspark", "kafka", "airflow", "hadoop", "hive", "etl", "elt", "redshift", "snowflake", "bigquery", "databricks", "dbt"],
    "Machine Learning & AI": ["scikit-learn", "sklearn", "pytorch", "tensorflow", "keras", "opencv", "transformers", "nlp", "cnn", "bert", "llm", "rag", "langchain", "crewai", "ollama"],
    "Databases": ["postgresql", "mysql", "sqlite", "mongodb", "redis", "cassandra", "dynamodb", "oracle", "chromadb"],
    "Cloud & DevOps": ["docker", "kubernetes", "git", "github", "aws", "gcp", "azure", "jenkins", "terraform", "ansible", "ci/cd"]
}

class ResumeAgent:
    def __init__(self):
        pass

    def extract_text_from_pdf(self, pdf_file_path):
        """
        Extracts raw text from a PDF resume.
        """
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

    def parse_resume(self, text_or_path):
        """
        Parses resume text or PDF file and returns extracted skills matrix and recommended role.
        """
        if text_or_path.lower().endswith(".pdf"):
            text = self.extract_text_from_pdf(text_or_path)
        else:
            text = text_or_path

        if not text:
            return {
                "skills": [],
                "skills_by_domain": {},
                "recommended_role": "Python Developer",
                "text_length": 0
            }

        text_lower = text.lower()
        extracted_skills = {}
        total_skills_count = 0

        for domain, keywords in SKILL_DOMAINS.items():
            found_in_domain = []
            for kw in keywords:
                pattern = r'\b' + kw + r'\b'
                if re.search(pattern, text_lower):
                    display_kw = kw.replace("\\", "").upper()
                    found_in_domain.append(display_kw)
            if found_in_domain:
                extracted_skills[domain] = found_in_domain
                total_skills_count += len(found_in_domain)

        role_scores = {
            "Python Developer": 0,
            "Data Analyst": 0,
            "Data Engineer": 0,
            "Machine Learning Engineer": 0,
            "DevOps / Cloud Engineer": 0,
            "Full Stack Developer": 0,
            "Backend Engineer": 0,
            "AI / LLM Engineer": 0
        }

        all_skills_flat = [s for sublist in extracted_skills.values() for s in sublist]

        # Scoring heuristics
        for s in all_skills_flat:
            if s in ["PYTHON", "DJANGO", "FLASK", "FASTAPI"]:
                role_scores["Python Developer"] += 3
                role_scores["Backend Engineer"] += 2

            if s in ["SQL", "PANDAS", "NUMPY", "EXCEL", "MYSQL", "POSTGRESQL"]:
                role_scores["Data Analyst"] += 2

            if s in ["SPARK", "PYSPARK", "KAFKA", "AIRFLOW", "HADOOP", "ETL", "ELT", "SNOWFLAKE", "REDSHIFT"]:
                role_scores["Data Engineer"] += 3

            if s in ["PYTORCH", "TENSORFLOW", "SCIKIT-LEARN", "NLP", "CNN", "TRANSFORMERS"]:
                role_scores["Machine Learning Engineer"] += 3

            if s in ["LLM", "RAG", "LANGCHAIN", "CREWAI", "OLLAMA", "TRANSFORMERS", "BERT"]:
                role_scores["AI / LLM Engineer"] += 4

            if s in ["DOCKER", "KUBERNETES", "AWS", "GCP", "AZURE", "TERRAFORM", "JENKINS", "ANSIBLE"]:
                role_scores["DevOps / Cloud Engineer"] += 3

            if s in ["REACT", "NODE", "JAVASCRIPT", "TYPESCRIPT", "HTML", "CSS", "NEXT.JS"]:
                role_scores["Full Stack Developer"] += 3

            if s in ["JAVA", "GOLANG", "C++", "REDIS", "POSTGRESQL", "MONGODB", "FASTAPI"]:
                role_scores["Backend Engineer"] += 2

        recommended_role = max(role_scores, key=role_scores.get)

        if total_skills_count == 0 or role_scores[recommended_role] == 0:
            recommended_role = "Python Developer"

        return {
            "skills": all_skills_flat,
            "skills_by_domain": extracted_skills,
            "recommended_role": recommended_role,
            "text_length": len(text)
        }

if __name__ == "__main__":
    agent = ResumeAgent()
    sample = "Skills: Python, PyTorch, LangChain, RAG, Ollama, Docker, LLM."
    res = agent.parse_resume(sample)
    print("Recommended Role:", res["recommended_role"])
    print("Skills:", res["skills"])
