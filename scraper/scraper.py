import os
import sys
import requests
from bs4 import BeautifulSoup
import re

# Ensure folders exist
os.makedirs("datasets/raw", exist_ok=True)

# 1. Local Seed Datasets (Fallback & Enrichment)
# Contains curated, high-quality technical interview questions and answers for each role.
LOCAL_KNOWLEDGE = {
    "python": [
        {
            "question": "What is the difference between a list and a tuple in Python?",
            "answer": "Lists are mutable, meaning their elements can be modified, added, or removed after creation. They are defined using square brackets []. Tuples are immutable, meaning they cannot be changed after creation. They are defined using parentheses () and are generally faster and consume less memory than lists."
        },
        {
            "question": "How is memory managed in Python?",
            "answer": "Memory management in Python is handled by the Python Memory Manager. It includes a private heap containing all Python objects and data structures. Python uses an automatic garbage collector that employs reference counting to track objects and garbage collect them when their reference count drops to zero. Additionally, a generational garbage collector handles cycle detection for self-referencing objects."
        },
        {
            "question": "What are decorators in Python and how do they work?",
            "answer": "Decorators are a design pattern in Python that allows a user to add new functionality to an existing object (typically a function or class) without modifying its structure. They are represented by the @decorator_name syntax and are executed before the function they decorate. Decorators are essentially wrapper functions that take a function as an argument and return a modified function."
        },
        {
            "question": "What is the difference between deep copy and shallow copy in Python?",
            "answer": "A shallow copy constructs a new compound object and then inserts references into it to the objects found in the original. Modifications to nested mutable objects in the copy will affect the original. A deep copy constructs a new compound object and then, recursively, inserts copies into it of the objects found in the original. Changes to the copy do not affect the original."
        },
        {
            "question": "Explain the difference between generator functions and regular functions.",
            "answer": "A regular function executes fully and returns a value using the 'return' keyword, destroying its local state. A generator function returns an iterator (generator object) and yields values one at a time using the 'yield' keyword. When a generator is called, it pauses execution and resumes from the last 'yield' statement when next() is called, preserving its local state."
        },
        {
            "question": "What are *args and **kwargs in Python function definitions?",
            "answer": "*args is used to pass a non-keyworded, variable-length argument list to a function, which is received as a tuple. **kwargs is used to pass a keyworded, variable-length argument list, which is received as a dictionary. They allow functions to accept arbitrary numbers of arguments dynamically."
        },
        {
            "question": "What is list comprehension and why is it preferred?",
            "answer": "List comprehension is a syntactic construct in Python for creating a new list based on existing lists or iterables. It provides a concise way to create lists, e.g., [x*x for x in range(10)]. It is generally faster than manual for-loops because it is optimized in C under the hood, and it makes code more readable when kept simple."
        },
        {
            "question": "What is the Global Interpreter Lock (GIL) and how does it affect concurrency?",
            "answer": "The Global Interpreter Lock (GIL) is a mutex that protects access to Python objects, preventing multiple threads from executing Python bytecodes at once in the CPython implementation. This lock is necessary because CPython's memory management is not thread-safe. As a result, CPU-bound multi-threaded programs do not see speedups in Python, and developers use multiprocessing or asynchronous programming instead."
        },
        {
            "question": "Explain the difference between __str__ and __repr__ in Python classes.",
            "answer": "__str__ is designed to return a user-friendly, readable string representation of an object, meant for end-users (triggered by print() or str()). __repr__ is designed to return an unambiguous representation of the object, primarily for developers and debugging (triggered by repr() or viewing in the interpreter), which ideally can be used to recreate the object."
        },
        {
            "question": "How do you handle exceptions in Python? Explain try-except-else-finally.",
            "answer": "Exceptions are handled using the try-except block. The 'try' block contains code that might raise an exception. The 'except' block catches and handles specific exceptions. The 'else' block runs if no exceptions were raised in the try block. The 'finally' block executes regardless of whether an exception occurred, and is typically used for cleanups like closing files or connections."
        }
    ],
    "sql": [
        {
            "question": "What is the difference between INNER JOIN, LEFT JOIN, RIGHT JOIN, and FULL JOIN?",
            "answer": "INNER JOIN returns records that have matching values in both tables. LEFT JOIN (or LEFT OUTER JOIN) returns all records from the left table, and matching records from the right table; if no match, it returns NULL for the right side. RIGHT JOIN returns all records from the right table, and matching records from the left. FULL JOIN returns all records when there is a match in either left or right table."
        },
        {
            "question": "Explain SQL injection and how to prevent it.",
            "answer": "SQL injection is a security vulnerability where an attacker injects malicious SQL statements into inputs, manipulating the database execution. To prevent SQL injection, you should use parameterized queries (prepared statements) instead of string concatenation, use stored procedures, validate user inputs, and restrict database user privileges."
        },
        {
            "question": "What is the difference between WHERE and HAVING clauses?",
            "answer": "The WHERE clause is used to filter records before any groupings are made (it acts on individual rows). The HAVING clause is used to filter groups created by the GROUP BY clause (it acts on aggregated rows). WHERE cannot contain aggregate functions (like SUM, AVG), whereas HAVING can."
        },
        {
            "question": "What are indexes in SQL and what are their pros and cons?",
            "answer": "Indexes are special lookup tables that the database search engine can use to speed up data retrieval. The main advantage is faster SELECT query execution. The disadvantages are that indexes require additional disk space and slow down write operations (INSERT, UPDATE, DELETE) because the database must update the index whenever the data changes."
        },
        {
            "question": "What are the differences between primary key, unique key, and foreign key?",
            "answer": "A primary key uniquely identifies each record in a table, must contain unique values, and cannot contain NULLs; a table can only have one primary key. A unique key also ensures uniqueness but can contain NULL values (usually only one depending on DB engine), and a table can have multiple unique keys. A foreign key is a field in one table that uniquely identifies a row in another table, establishing a relationship between them."
        },
        {
            "question": "Explain database normalization and its forms (1NF, 2NF, 3NF).",
            "answer": "Normalization is the process of organizing data in a database to reduce redundancy and improve data integrity. First Normal Form (1NF) requires atomic values and no repeating groups. Second Normal Form (2NF) meets 1NF and requires all non-key columns to be fully dependent on the primary key. Third Normal Form (3NF) meets 2NF and requires no transitive dependencies (non-key columns must depend only on the primary key)."
        },
        {
            "question": "What are window functions in SQL and how do they work?",
            "answer": "Window functions perform calculations across a set of table rows that are somehow related to the current row, without grouping the output into a single row. They use the OVER() clause to define the window partition and ordering. Common window functions include ROW_NUMBER(), RANK(), DENSE_RANK(), LAG(), and LEAD()."
        },
        {
            "question": "What is the difference between UNION and UNION ALL?",
            "answer": "Both UNION and UNION ALL combine result sets of two or more SELECT queries into a single result set. UNION removes duplicate rows from the final result set, which requires a sorting operation, making it slower. UNION ALL returns all rows including duplicates, which is faster because it does not perform duplicate checking."
        },
        {
            "question": "What is ACID in database transactions?",
            "answer": "ACID is a set of properties that guarantee database transactions are processed reliably: Atomicity (all operations in a transaction succeed or all fail); Consistency (transaction brings the database from one valid state to another); Isolation (concurrent transactions execute without interfering); and Durability (once committed, changes survive system crashes)."
        },
        {
            "question": "Explain the difference between DELETE, TRUNCATE, and DROP statements.",
            "answer": "DELETE is a DML command used to remove specific rows from a table using a WHERE clause; it can be rolled back and triggers database triggers. TRUNCATE is a DDL command that removes all rows from a table, releasing storage; it is faster because it bypasses logging individual row deletes, cannot be rolled back easily in some systems, and does not trigger triggers. DROP is a DDL command that removes the entire table structure and its data completely from the database."
        }
    ],
    "data_engineer": [
        {
            "question": "What is ETL and how does it differ from ELT?",
            "answer": "ETL stands for Extract, Transform, Load, where data is extracted from sources, transformed on a staging server, and then loaded into a target database (like a Data Warehouse). ELT stands for Extract, Load, Transform, where data is extracted and immediately loaded into the target (like a modern Cloud Data Warehouse or Lakehouse), leveraging the target's compute resources to perform transformations. ELT is faster and handles raw unstructured data better."
        },
        {
            "question": "Explain Apache Spark's architecture and how it achieves distributed processing.",
            "answer": "Apache Spark uses a master-slave architecture. It consists of a Driver Program (coordinates applications, schedules tasks, runs main()) and Executors (worker nodes that run individual tasks and store data). The Cluster Manager (YARN, Mesos, or Spark Standalone) allocates resources. Spark achieves fast distributed processing by keeping data in-memory across the cluster and creating a Directed Acyclic Graph (DAG) of transformations, optimizing execution before running actions."
        },
        {
            "question": "What is Apache Kafka and what are its key components?",
            "answer": "Apache Kafka is a distributed event streaming platform. Key components include: Producers (publish events to topics); Consumers (subscribe to topics and read events); Brokers (servers that form the Kafka cluster and store topics); Topics (categories or feed names to which messages are published); Partitions (topics are split into partitions for scalability and parallelism); and Consumer Groups (groups of consumers that read data concurrently without duplicating messages)."
        },
        {
            "question": "What is a star schema and snowflake schema in data warehousing?",
            "answer": "A star schema is a dimensional modeling design where a central Fact Table (containing business metrics/keys) is connected directly to multiple Dimension Tables (describing business attributes), resembling a star. A snowflake schema is a variation where dimension tables are normalized into multiple related tables, reducing redundancy but increasing the number of joins needed in queries."
        },
        {
            "question": "What is Apache Airflow and how does it work?",
            "answer": "Apache Airflow is an open-source platform used to programmatically author, schedule, and monitor workflows. Workflows are defined as Directed Acyclic Graphs (DAGs) in Python. Airflow consists of a Webserver (UI), Scheduler (triggers workflows and sends tasks to workers), Database (stores state), and Executor/Workers (executes tasks). Airflow uses Tasks representing operators (BashOperator, PythonOperator, etc.) to perform work."
        },
        {
            "question": "Explain the difference between batch processing and stream processing.",
            "answer": "Batch processing involves processing large volumes of data collected over a period of time, executed in scheduled runs (e.g. daily, hourly) where latency is not critical (e.g. Apache Spark, Hadoop). Stream processing involves ingestion and processing of data in real-time or near-real-time as it is generated (e.g. Apache Flink, Spark Streaming, Kafka Streams), characterized by low latency and continuous execution."
        },
        {
            "question": "What is a Data Lake, Data Warehouse, and Lakehouse?",
            "answer": "A Data Warehouse is a structured repository optimized for SQL analytics and reporting, storing cleaned relational data. A Data Lake is a repository that stores massive amounts of raw, unstructured, semi-structured, and structured data in native format (e.g. S3, HDFS). A Data Lakehouse (like Databricks or Apache Iceberg) combines both, offering the cheap storage and flexibility of a Data Lake along with ACID transactions, schema enforcement, and SQL analytics of a Data Warehouse."
        },
        {
            "question": "What are partitions and bucketing in Hive/Spark and why are they used?",
            "answer": "Partitions split a table physically based on a column value (e.g. date, country), creating subdirectories. It prevents full table scans by only reading matching subdirectories. Bucketing (or clustering) splits data into a fixed number of buckets using a hash function on a specific column. It optimizes join performance (bucket map joins) and improves query performance on high-cardinality columns."
        },
        {
            "question": "How do you handle schema evolution in data pipelines?",
            "answer": "Schema evolution is handled by choosing file formats that support schema metadata (like Avro, Parquet, or Protocol Buffers) and using a Schema Registry (like Confluent Schema Registry in Kafka). Pipelines can handle changes in schema (like adding new columns, dropping columns, or modifying data types) by applying backward, forward, or full compatibility rules to prevent downstream analytics from breaking."
        },
        {
            "question": "What is change data capture (CDC) and how is it implemented?",
            "answer": "Change Data Capture (CDC) is a technique used to identify and capture insertion, update, and deletion changes in a source database and deliver them to target systems in real-time. It can be implemented using query-based methods (polling updated_at columns), trigger-based methods (database triggers writing to log tables), or log-based methods (reading database transaction logs using tools like Debezium), which is the most efficient and least intrusive method."
        }
    ],
    "ml": [
        {
            "question": "What is the difference between supervised and unsupervised learning?",
            "answer": "Supervised learning involves training a model on a labeled dataset, meaning each training example is paired with its correct output label (e.g. classification, regression). Unsupervised learning involves training a model on unlabeled data, where the algorithm must find patterns, structures, or groupings on its own (e.g. clustering like K-Means, dimensionality reduction like PCA)."
        },
        {
            "question": "Explain the bias-variance tradeoff in Machine Learning.",
            "answer": "The bias-variance tradeoff represents the struggle to minimize two sources of error: Bias (error from erroneous assumptions in the model, leading to underfitting because the model is too simple); and Variance (error from sensitivity to small fluctuations in the training set, leading to overfitting because the model is too complex and captures noise). High bias models fail to capture training patterns, while high variance models fail to generalize to validation data."
        },
        {
            "question": "What is overfitting and how do you prevent it?",
            "answer": "Overfitting occurs when a model learns the training data too well, including its noise and outliers, failing to generalize to unseen test data. To prevent overfitting, you can: collect more training data; simplify the model; use regularization (L1/L2 Lasso/Ridge); apply dropout in neural networks; perform cross-validation; use ensemble methods (e.g., Random Forests); or implement early stopping."
        },
        {
            "question": "Explain the difference between L1 (Lasso) and L2 (Ridge) regularization.",
            "answer": "L1 regularization (Lasso) adds the absolute values of the coefficients as a penalty term to the loss function, forcing some coefficients to become exactly zero, which performs automatic feature selection. L2 regularization (Ridge) adds the squared values of the coefficients as a penalty term, shrinking coefficients towards zero but never making them exactly zero, which keeps all features but reduces their magnitude."
        },
        {
            "question": "How do you evaluate a classification model? Explain Precision, Recall, F1-Score.",
            "answer": "Classification models are evaluated using: Precision (True Positives / (True Positives + False Positives)), which measures the accuracy of positive predictions; Recall (True Positives / (True Positives + False Negatives)), which measures the percentage of actual positives correctly identified; and F1-Score (2 * (Precision * Recall) / (Precision + Recall)), which is the harmonic mean of precision and recall, balancing both metrics, especially in imbalanced datasets."
        },
        {
            "question": "What is the gradient descent algorithm and how does it work?",
            "answer": "Gradient descent is an optimization algorithm used to minimize the cost function of a model by iteratively moving in the direction of steepest descent (negative gradient). The step size is determined by the learning rate. In Stochastic Gradient Descent (SGD), the gradient is updated per sample; in Batch Gradient Descent, it is calculated across the entire dataset; and in Mini-Batch Gradient Descent, it is calculated across small subsets."
        },
        {
            "question": "Explain how a Random Forest model works.",
            "answer": "Random Forest is an ensemble learning method that builds multiple Decision Trees during training and merges their outputs (voting for classification, averaging for regression) to get a more accurate and stable prediction. It uses Bagging (Bootstrap Aggregating) to train individual trees on random subsets of the data, and selects random subsets of features at each split point to ensure the trees are decorrelated, reducing variance."
        },
        {
            "question": "What is the difference between K-Means and KNN (K-Nearest Neighbors)?",
            "answer": "K-Means is an unsupervised clustering algorithm used to group data points into K clusters based on distance to cluster centroids. KNN is a supervised classification/regression algorithm that predicts the label of a new data point by looking at the majority vote of its K closest labeled neighbors in the training dataset."
        },
        {
            "question": "What are transformer models in NLP and what is the self-attention mechanism?",
            "answer": "Transformer models are a deep learning architecture that processes sequential data in parallel, unlike RNNs. The self-attention mechanism allows the model to dynamic calculate the relationship between different words in a sentence, regardless of their distance. It computes Query, Key, and Value vectors for each word, producing weighted context representations that capture long-range dependencies efficiently."
        },
        {
            "question": "Explain the concept of cross-validation.",
            "answer": "Cross-validation is a resampling technique used to evaluate machine learning models on a limited data sample. In K-Fold Cross-Validation, the dataset is split into K equal subsets. The model is trained on K-1 subsets and evaluated on the remaining 1 subset. This process is repeated K times, with each subset used as the test set exactly once. The results are averaged to get an unbiased estimate of model performance."
        }
    ]
}

# 2. Online Scraper Targets (GitHub Markdown / Public Resources)
ONLINE_TARGETS = {
    "python": [
        "https://raw.githubusercontent.com/learning-zone/python-interview-questions/master/README.md",
        "https://raw.githubusercontent.com/swaroopch/byte-of-python/master/README.md"
    ],
    "sql": [
        "https://raw.githubusercontent.com/readytocode/SQL-Interview-Questions/master/README.md",
        "https://raw.githubusercontent.com/Karan-S-Gyanani/SQL-Interview-Questions/master/README.md"
    ],
    "data_engineer": [
        "https://raw.githubusercontent.com/data-engineering-community/data-engineering-wiki/main/docs/interview-questions.md",
        "https://raw.githubusercontent.com/andkret/Cookbook/master/sections/data-engineering-interview-questions.md"
    ],
    "ml": [
        "https://raw.githubusercontent.com/andreis/interview-questions/master/machine-learning.md",
        "https://raw.githubusercontent.com/khanguyen19/ml-cheat-sheet/master/README.md"
    ]
}

def clean_markdown(text):
    """
    Remove basic markdown styling to extract raw question and answers.
    """
    # Replace markdown headers, bold, italics, code blocks
    text = re.sub(r'#+\s+', '', text)
    text = re.sub(r'\*\*|__', '', text)
    text = re.sub(r'`', '', text)
    return text.strip()

def scrape_url(url):
    """
    Fetch raw text or HTML content from a URL.
    If it is markdown (raw github), return content.
    If HTML, extract text using BeautifulSoup.
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            if "raw.githubusercontent.com" in url or url.endswith(".md"):
                return response.text
            else:
                soup = BeautifulSoup(response.content, 'html.parser')
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.extract()
                return soup.get_text(separator="\n")
    except Exception as e:
        print(f"  [Scrape Error] Failed to scrape {url}: {e}", file=sys.stderr)
    return ""

def main():
    print("="*60)
    print("HYBRID INTERVIEW QUESTIONS DATA scraper")
    print("="*60)

    for role, urls in ONLINE_TARGETS.items():
        print(f"\nProcessing Role: {role.upper()}")
        scraped_content = []

        # Attempt to scrape online sources
        for url in urls:
            print(f"  Attempting to fetch: {url}")
            content = scrape_url(url)
            if content:
                print(f"    [Success] Fetched {len(content)} characters of content.")
                # Basic parsing to extract Q&A patterns from markdown
                # Look for bullet points or headings with questions
                lines = content.split('\n')
                current_q = ""
                current_a = []
                for line in lines:
                    line = line.strip()
                    # Pattern matching for questions
                    if re.match(r'^(?:\d+\.|\*|-)\s*(?:What|How|Explain|Why|Describe|Is|Difference|Define|Write|Can)\b', line, re.IGNORECASE):
                        if current_q and current_a:
                            scraped_content.append({
                                "question": clean_markdown(current_q),
                                "answer": clean_markdown(" ".join(current_a))
                            })
                            current_a = []
                        current_q = re.sub(r'^(?:\d+\.|\*|-)\s*', '', line)
                    elif current_q and line:
                        current_a.append(line)
                
                # Append last
                if current_q and current_a:
                    scraped_content.append({
                        "question": clean_markdown(current_q),
                        "answer": clean_markdown(" ".join(current_a))
                    })
            else:
                print(f"    [Skip] Could not retrieve or empty response.")

        # Load local seed questions
        local_seed = LOCAL_KNOWLEDGE.get(role, [])
        print(f"  Loaded {len(local_seed)} local seed questions.")

        # Combine online scraped and local questions
        # Prioritize local seed, avoid duplicates by question text overlap
        all_questions = []
        seen_questions = set()

        for item in local_seed:
            q_norm = re.sub(r'\W+', '', item["question"].lower())
            all_questions.append(item)
            seen_questions.add(q_norm)

        for item in scraped_content:
            q_norm = re.sub(r'\W+', '', item["question"].lower())
            if q_norm not in seen_questions and len(item["question"]) > 15 and len(item["answer"]) > 15:
                all_questions.append(item)
                seen_questions.add(q_norm)

        print(f"  Total consolidated questions collected: {len(all_questions)}")

        # Write to raw files
        raw_file_path = f"datasets/raw/{role}_questions.txt"
        with open(raw_file_path, "w", encoding="utf-8") as f:
            for idx, item in enumerate(all_questions):
                f.write(f"QUESTION {idx+1}: {item['question']}\n")
                f.write(f"ANSWER {idx+1}: {item['answer']}\n")
                f.write("="*40 + "\n")
        
        print(f"  Saved raw questions to: {raw_file_path}")

    print("\n" + "="*60)
    print("[SUCCESS] Data collection complete.")
    print("="*60)

if __name__ == "__main__":
    main()
