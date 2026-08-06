import os
import pandas as pd
import re

# Ensure directory exists
os.makedirs("datasets/processed", exist_ok=True)

ROLE_MAP = {
    "python": "Python Developer",
    "sql": "Data Analyst",
    "data_engineer": "Data Engineer",
    "ml": "Machine Learning Engineer"
}

def infer_topic(role, question, answer):
    """
    Heuristically infer the sub-topic of a question-answer pair.
    """
    text = (question + " " + answer).lower()
    
    if role == "python":
        if "gil" in text or "interpreter lock" in text:
            return "Global Interpreter Lock"
        elif "decorator" in text:
            return "Decorators"
        elif "generator" in text or "yield" in text:
            return "Generators & Iterators"
        elif "copy" in text and ("deep" in text or "shallow" in text):
            return "Memory & Copying"
        elif "list" in text and "tuple" in text:
            return "Data Structures"
        elif "memory" in text or "garbage collector" in text:
            return "Memory Management"
        elif "args" in text or "kwargs" in text:
            return "Function Arguments"
        elif "comprehension" in text:
            return "List Comprehension"
        elif "exception" in text or "try" in text or "except" in text:
            return "Exception Handling"
        else:
            return "Python Core"
            
    elif role == "sql":
        if "join" in text:
            return "SQL Joins"
        elif "index" in text:
            return "Indexing"
        elif "where" in text and "having" in text:
            return "Filtering & Grouping"
        elif "primary" in text or "foreign" in text or "unique" in text:
            return "Keys & Constraints"
        elif "normalization" in text:
            return "Database Normalization"
        elif "window" in text or "over(" in text or "row_number" in text:
            return "Window Functions"
        elif "union" in text:
            return "Set Operations"
        elif "acid" in text or "transaction" in text:
            return "Transactions"
        elif "delete" in text or "truncate" in text or "drop" in text:
            return "DDL vs DML"
        elif "injection" in text:
            return "Database Security"
        else:
            return "SQL Core"
            
    elif role == "data_engineer":
        if "etl" in text or "elt" in text:
            return "ETL/ELT Pipelines"
        elif "spark" in text:
            return "Apache Spark"
        elif "kafka" in text:
            return "Apache Kafka"
        elif "star" in text or "snowflake" in text or "dimension" in text:
            return "Data Warehousing"
        elif "airflow" in text or "dag" in text:
            return "Workflow Orchestration"
        elif "lake" in text or "lakehouse" in text:
            return "Data Lakehouse"
        elif "batch" in text or "stream" in text:
            return "Data Processing Modes"
        elif "partition" in text or "bucket" in text:
            return "Data Partitioning"
        elif "evolution" in text or "schema" in text:
            return "Schema Management"
        elif "cdc" in text or "change data" in text:
            return "Change Data Capture (CDC)"
        else:
            return "Data Engineering Core"
            
    elif role == "ml":
        if "supervised" in text or "unsupervised" in text:
            return "Learning Paradigms"
        elif "bias" in text or "variance" in text:
            return "Model Evaluation Heuristics"
        elif "overfit" in text or "underfit" in text:
            return "Regularization & Overfitting"
        elif "l1" in text or "l2" in text or "lasso" in text or "ridge" in text:
            return "Regularization"
        elif "precision" in text or "recall" in text or "f1" in text:
            return "Classification Metrics"
        elif "gradient descent" in text or "optimizer" in text:
            return "Optimization Algorithms"
        elif "random forest" in text or "ensemble" in text:
            return "Ensemble Methods"
        elif "k-means" in text or "knn" in text:
            return "Clustering & Classification"
        elif "transformer" in text or "attention" in text or "nlp" in text:
            return "Deep Learning & NLP"
        elif "cross-validation" in text:
            return "Model Validation"
        else:
            return "Machine Learning Core"
            
    return "General"

def infer_difficulty(question, answer):
    """
    Infer technical difficulty based on keyword complexity.
    """
    text = (question + " " + answer).lower()
    
    # Heuristics for Hard questions
    hard_keywords = [
        "gil", "garbage collector", "deep copy", "window function", 
        "normalization", "acid", "spark", "kafka", "dag", "cdc", 
        "bias-variance", "regularization", "gradient descent", 
        "transformer", "attention", "cross-validation"
    ]
    
    # Heuristics for Medium questions
    medium_keywords = [
        "decorator", "generator", "args", "kwargs", "index", 
        "having", "foreign key", "union", "etl", "elt", 
        "star schema", "data lake", "overfit", "precision", 
        "recall", "random forest", "k-means"
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
            
        # Split by separator
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
        # Drop exact duplicate questions
        df.drop_duplicates(subset=["Question"], inplace=True)
        
        output_csv = "datasets/processed/knowledge_base.csv"
        df.to_csv(output_csv, index=False, encoding="utf-8")
        
        print("\n" + "="*60)
        print("CONSOLIDATED KNOWLEDGE BASE SUMMARY")
        print("="*60)
        print(f"Total Rows Saved: {len(df)}")
        print("\nDistribution by Role:")
        print(df["Role"].value_counts().to_string())
        print("\nDistribution by Difficulty:")
        print(df["Difficulty"].value_counts().to_string())
        print("\nSaved Knowledge Base CSV to:", os.path.abspath(output_csv))
        print("="*60)
    else:
        print("[Error] No questions were found to compile.")

if __name__ == "__main__":
    main()
