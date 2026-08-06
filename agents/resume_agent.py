import re
import PyPDF2

# Predefined skill keywords for pattern matching
SKILL_DOMAINS = {
    "Languages": ["python", "sql", "java", "c\\+\\+", "javascript", "scala", "golang", "r", "bash", "html", "css"],
    "Python Frameworks": ["django", "flask", "fastapi", "numpy", "pandas", "scipy", "celery", "poetry"],
    "Data Engineering": ["spark", "pyspark", "kafka", "airflow", "hadoop", "hive", "etl", "elt", "redshift", "snowflake", "bigquery", "databricks", "dbt", "glues", "fargate"],
    "Machine Learning & DL": ["scikit-learn", "sklearn", "pytorch", "tensorflow", "keras", "opencv", "transformers", "nlp", "cnn", "rnn", "lstm", "bert", "llm", "deep learning", "machine learning"],
    "Databases": ["postgresql", "mysql", "sqlite", "mongodb", "redis", "cassandra", "dynamodb", "oracle"],
    "Tools & DevOps": ["docker", "kubernetes", "git", "github", "aws", "gcp", "azure", "jenkins", "terraform", "ansible"]
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
        Parses resume text (or extracts it from a PDF path) and extracts:
        - Found Skills
        - Recommended Role
        - Identified Keywords
        """
        # If a file path is provided, extract text first
        if text_or_path.lower().endswith(".pdf"):
            text = self.extract_text_from_pdf(text_or_path)
        else:
            text = text_or_path

        if not text:
            return {
                "skills": [],
                "recommended_role": "Python Developer",
                "extracted_info": {}
            }

        text_lower = text.lower()
        extracted_skills = {}
        total_skills_count = 0

        # Scan for skills across predefined domains
        for domain, keywords in SKILL_DOMAINS.items():
            found_in_domain = []
            for kw in keywords:
                # Use regex word boundaries for precise matching
                pattern = r'\b' + kw + r'\b'
                if re.search(pattern, text_lower):
                    # Clean display formatting
                    display_kw = kw.replace("\\", "").upper()
                    found_in_domain.append(display_kw)
            if found_in_domain:
                extracted_skills[domain] = found_in_domain
                total_skills_count += len(found_in_domain)

        # Heuristic to recommend a role based on skills count
        role_scores = {
            "Python Developer": 0,
            "Data Analyst": 0,
            "Data Engineer": 0,
            "Machine Learning Engineer": 0
        }

        # Calculate role weights
        all_skills_flat = [s for sublist in extracted_skills.values() for s in sublist]
        
        # Python Developer weights
        for s in ["PYTHON", "DJANGO", "FLASK", "FASTAPI", "GIT", "POSTGRESQL"]:
            if s in all_skills_flat:
                role_scores["Python Developer"] += 2
                
        # Data Analyst weights
        for s in ["SQL", "PANDAS", "NUMPY", "EXCEL", "POSTGRESQL", "MYSQL"]:
            if s in all_skills_flat:
                role_scores["Data Analyst"] += 2
                
        # Data Engineer weights
        for s in ["SPARK", "PYSPARK", "KAFKA", "AIRFLOW", "HADOOP", "ETL", "ELT", "SNOWFLAKE", "SCALA"]:
            if s in all_skills_flat:
                role_scores["Data Engineer"] += 3

        # ML Engineer weights
        for s in ["PYTORCH", "TENSORFLOW", "SCIKIT-LEARN", "TRANSFORMERS", "NLP", "MACHINE LEARNING", "DEEP LEARNING", "LLM"]:
            if s in all_skills_flat:
                role_scores["Machine Learning Engineer"] += 3

        # Add generic weights based on languages
        if "PYTHON" in all_skills_flat:
            role_scores["Python Developer"] += 1
            role_scores["Machine Learning Engineer"] += 1
            role_scores["Data Engineer"] += 1
        if "SQL" in all_skills_flat:
            role_scores["Data Analyst"] += 1
            role_scores["Data Engineer"] += 1

        # Determine recommended role
        recommended_role = max(role_scores, key=role_scores.get)
        
        # If no skills found, default to Python Developer
        if total_skills_count == 0:
            recommended_role = "Python Developer"

        return {
            "skills": all_skills_flat,
            "skills_by_domain": extracted_skills,
            "recommended_role": recommended_role,
            "text_length": len(text)
        }

if __name__ == "__main__":
    # Test parser with simulated resume text
    agent = ResumeAgent()
    sample_resume = """
    John Doe - Data Pipeline Engineer
    Skills: Python, SQL, Apache Spark, PySpark, Apache Kafka, Apache Airflow.
    Databases: PostgreSQL, MongoDB.
    Tools: Docker, Git, AWS.
    Experience in building scalable ETL pipelines.
    """
    res = agent.parse_resume(sample_resume)
    print("[Test] Recommended Role:", res["recommended_role"])
    print("[Test] Extracted Skills:", res["skills"])
    print("[Test] Skills by Domain:", res["skills_by_domain"])
