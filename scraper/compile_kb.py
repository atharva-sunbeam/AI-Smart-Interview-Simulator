import os
import pandas as pd
import re

os.makedirs("datasets/processed", exist_ok=True)

ROLE_MAP = {
    "python": "Python Developer",
    "sql": "Data Analyst",
    "data_engineer": "Data Engineer",
    "ml": "Machine Learning Engineer",
    "devops": "DevOps / Cloud Engineer",
    "fullstack": "Full Stack Developer",
    "backend": "Backend Engineer",
    "ai_llm": "AI / LLM Engineer"
}

def infer_topic(role, question, answer):
    text = (question + " " + answer).lower()
    
    if role == "devops":
        if "docker" in text or "container" in text:
            return "Containerization & Docker"
        elif "kubernetes" in text or "pod" in text or "ingress" in text:
            return "Kubernetes & Orchestration"
        elif "terraform" in text or "iac" in text:
            return "Infrastructure as Code"
        elif "ci/cd" in text or "pipeline" in text or "jenkins" in text:
            return "CI/CD Automation"
        elif "aws" in text or "iam" in text or "cloud" in text:
            return "Cloud Architecture & Security"
        elif "blue-green" in text or "canary" in text:
            return "Deployment Strategies"
        else:
            return "DevOps & Cloud Core"

    elif role == "ai_llm":
        if "rag" in text or "retrieval" in text:
            return "RAG Architecture"
        elif "vector" in text or "embedding" in text or "chromadb" in text:
            return "Vector DBs & Embeddings"
        elif "langchain" in text or "agent" in text or "crewai" in text:
            return "LLM Agents & Tools"
        elif "quantization" in text or "gguf" in text:
            return "Model Quantization & Inference"
        elif "hallucination" in text:
            return "LLM Safety & Guardrails"
        elif "fine-tuning" in text or "lora" in text:
            return "Fine-Tuning vs In-Context Learning"
        else:
            return "AI & LLM Core"

    elif role == "fullstack":
        if "ssr" in text or "csr" in text or "rendering" in text:
            return "Rendering Strategies"
        elif "virtual dom" in text or "react" in text or "hooks" in text:
            return "Frontend Frameworks (React)"
        elif "event loop" in text or "node" in text:
            return "Asynchronous Runtime"
        elif "cors" in text or "security" in text or "xss" in text:
            return "Web Security & CORS"
        elif "websocket" in text or "rest" in text:
            return "API Protocols"
        else:
            return "Full Stack Core"

    elif role == "backend":
        if "b-tree" in text or "index" in text:
            return "Database Indexing & Performance"
        elif "cache" in text or "redis" in text:
            return "Caching Strategies"
        elif "microservice" in text or "monolith" in text:
            return "Microservices Architecture"
        elif "n+1" in text or "orm" in text:
            return "ORM & Data Access"
        elif "message queue" in text or "kafka" in text:
            return "Event Streaming & Queues"
        elif "cap" in text or "shard" in text:
            return "Distributed Systems"
        else:
            return "Backend Core"

    elif role == "python":
        if "gil" in text:
            return "Global Interpreter Lock"
        elif "decorator" in text:
            return "Decorators"
        elif "generator" in text:
            return "Generators & Iterators"
        elif "copy" in text:
            return "Memory & Copying"
        else:
            return "Python Core"
            
    elif role == "sql":
        if "join" in text:
            return "SQL Joins"
        elif "index" in text:
            return "Indexing"
        elif "window" in text:
            return "Window Functions"
        else:
            return "SQL Core"
            
    elif role == "data_engineer":
        if "spark" in text:
            return "Apache Spark"
        elif "kafka" in text:
            return "Apache Kafka"
        elif "etl" in text:
            return "ETL/ELT Pipelines"
        else:
            return "Data Engineering Core"
            
    elif role == "ml":
        if "bias" in text or "variance" in text:
            return "Model Evaluation"
        elif "overfit" in text or "regularization" in text:
            return "Regularization & Overfitting"
        else:
            return "Machine Learning Core"
            
    return "General"

def infer_difficulty(question, answer):
    text = (question + " " + answer).lower()
    
    hard_keywords = [
        "gil", "garbage collector", "kubernetes", "ingress", "disaster recovery",
        "quantization", "gguf", "transformer", "attention", "b-tree", "sharding",
        "cap theorem", "n+1", "cache stampede", "reconciliation", "state hydration"
    ]
    medium_keywords = [
        "decorator", "generator", "docker", "terraform", "ci/cd", "rag",
        "embedding", "vector", "langchain", "ssr", "csr", "cors", "event loop",
        "react", "cache-aside", "microservice", "spark", "kafka", "star schema"
    ]
    
    if any(kw in text for kw in hard_keywords):
        return "Hard"
    elif any(kw in text for kw in medium_keywords):
        return "Medium"
    else:
        return "Easy"

def main():
    all_rows = []
    
    for file_role, display_role in ROLE_MAP.items():
        cleaned_path = f"datasets/cleaned/{file_role}_questions.txt"
        
        if not os.path.exists(cleaned_path):
            print(f"Cleaned file not found: {cleaned_path}")
            continue
            
        print(f"Compiling questions for {display_role}...")
        
        with open(cleaned_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        blocks = content.split("----------------------------------------")
        
        count = 0
        for block in blocks:
            block = block.strip()
            if not block:
                continue
                
            lines = block.split('\n')
            question = ""
            answer = ""
            
            for line in lines:
                line = line.strip()
                if line.startswith("Q:"):
                    question = line[2:].strip()
                elif line.startswith("A:"):
                    answer = line[2:].strip()
            
            if question and answer:
                topic = infer_topic(file_role, question, answer)
                difficulty = infer_difficulty(question, answer)
                
                all_rows.append({
                    "Role": display_role,
                    "Topic": topic,
                    "Question": question,
                    "Answer": answer,
                    "Difficulty": difficulty
                })
                count += 1
                
        print(f"  Added {count} questions.")

    if all_rows:
        df = pd.DataFrame(all_rows)
        df.drop_duplicates(subset=["Question"], inplace=True)
        
        output_csv = "datasets/processed/knowledge_base.csv"
        df.to_csv(output_csv, index=False, encoding="utf-8")
        
        print("\n" + "="*60)
        print("CONSOLIDATED KNOWLEDGE BASE SUMMARY")
        print("="*60)
        print(f"Total Rows Saved: {len(df)}")
        print("\nDistribution by Role:")
        print(df["Role"].value_counts().to_string())
        print("\nSaved Knowledge Base CSV to:", os.path.abspath(output_csv))
        print("="*60)

if __name__ == "__main__":
    main()
