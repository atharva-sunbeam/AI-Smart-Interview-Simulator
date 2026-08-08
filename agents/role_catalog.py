import re

# Catalog of supported engineering roles and blueprints

# Shared Tech Stack Clusters across engineering roles
TECH_STACK_CLUSTERS = {
    "Data_AI": [
        "Python Developer", "Data Analyst", "Business Intelligence Developer", "Data Engineer",
        "Machine Learning Engineer", "Deep Learning Engineer", "AI Engineer", "AI / LLM Engineer",
        "NLP Engineer", "Data Warehouse Engineer", "MLOps Engineer", "Big Data Developer", "Spark / Hadoop Engineer"
    ],
    "Infra_Cloud_Security": [
        "Linux System Administrator", "Network Administrator", "System Administrator", "Infrastructure Engineer",
        "Cyber Security Analyst", "SOC Analyst", "DevOps / Cloud Engineer", "Site Reliability Engineer (SRE)",
        "Cloud Architect", "Penetration Tester / Ethical Hacker", "Security Engineer", "Cloud Security Engineer",
        "DevOps Engineer", "Cloud Engineer (AWS / Azure / GCP)"
    ],
    "Software_Systems_Web": [
        "Full Stack Developer", "Backend Engineer", "Frontend Engineer", "Java Developer",
        "C++ Developer", "Software Testing Engineer", "Database Administrator", "Web Developer",
        "Embedded Systems Engineer", "Firmware Engineer", "IoT Developer", "Android App Developer", "Flutter Developer"
    ]
}

# Key technical domain indicator weights for role prediction
ROLE_KEYWORD_WEIGHTS = {
    "AI / LLM Engineer": [
        "llm", "llms", "large language models", "generative ai", "genai", "rag", "langchain", "crewai", "ollama",
        "vector databases", "chromadb", "faiss", "pinecone", "multi-agent", "ai agents", "transformers", "nlp", "bert"
    ],
    "AI Engineer": [
        "ai", "generative ai", "genai", "nlp", "computer vision", "opencv", "deep learning", "pytorch",
        "tensorflow", "keras", "neural networks", "multi-agent", "ai agents"
    ],
    "Machine Learning Engineer": [
        "machine learning", "practical machine learning", "ml", "data science", "scikit-learn", "sklearn", "pandas", "numpy",
        "feature engineering", "mlops", "model deployment", "predictive modeling", "xgboost", "lightgbm"
    ],
    "Deep Learning Engineer": [
        "deep learning", "neural networks", "cnn", "rnn", "pytorch", "tensorflow", "keras", "quantization", "computer vision"
    ],
    "NLP Engineer": [
        "nlp", "natural language processing", "bert", "transformers", "tokenization", "word embeddings", "word2vec"
    ],
    "Data Engineer": [
        "data engineer", "spark", "apache spark", "pyspark", "databricks", "hadoop", "etl", "kafka", "airflow", "sql", "delta lake", "big data"
    ],
    "Data Analyst": [
        "data analyst", "data visualization", "tableau", "power bi", "analytics", "advanced analytics", "statistics", "sql", "pandas", "reporting"
    ],
    "Big Data Developer": [
        "big data", "spark", "apache spark", "hadoop", "hdfs", "pyspark", "databricks", "kafka", "mapreduce"
    ],
    "Spark / Hadoop Engineer": [
        "spark", "apache spark", "hadoop", "hdfs", "pyspark", "databricks", "delta lake", "yarn"
    ],
    "Cloud Engineer (AWS / Azure / GCP)": [
        "aws", "gcp", "azure", "cloud", "ec2", "s3", "terraform", "ansible", "cloudformation", "vpc", "iam"
    ],
    "DevOps / Cloud Engineer": [
        "devops", "docker", "kubernetes", "k8s", "ci/cd", "jenkins", "terraform", "ansible", "prometheus", "grafana"
    ],
    "Linux System Administrator": [
        "linux", "sysadmin", "system administration", "bash", "shell scripting", "systemd", "lvm", "nfs", "ssh", "redhat", "centos", "ubuntu"
    ],
    "Python Developer": [
        "python", "fastapi", "django", "flask", "numpy", "pandas"
    ],
    "Java Developer": [
        "java", "spring", "spring boot", "hibernate", "maven"
    ],
    "C++ Developer": [
        "c++", "cpp"
    ],
    "Full Stack Developer": [
        "react", "vue", "angular", "node", "express", "next.js", "javascript", "typescript", "full stack"
    ]
}

def get_related_roles(role):
    """Returns sister roles sharing the same tech stack cluster."""
    for cluster_name, role_list in TECH_STACK_CLUSTERS.items():
        if role in role_list:
            return [r for r in role_list if r != role]
    return []


# Blueprint mappings for each job role
ROLE_BLUEPRINTS = {
    # ITISS Roles
    "Linux System Administrator": [
        "Linux CLI & File Operations",
        "User Management & Permissions",
        "Process Control & Systemd",
        "Disk Management & LVM",
        "Bash Shell Scripting & Automation",
        "Networking Services (SSH, DNS, DHCP, NFS)"
    ],
    "Network Administrator": [
        "OSI & TCP/IP Protocol Stack",
        "IP Addressing, CIDR & Subnetting",
        "Routing & Switching Fundamentals",
        "Firewalls, NAT & VPNs",
        "Network Diagnostics & Wireshark",
        "DNS, DHCP & Network Services"
    ],
    "System Administrator": [
        "OS Administration (Linux/Windows)",
        "Active Directory & User Authentication",
        "System Backup, Storage & LVM",
        "Scripting & System Automation",
        "System Monitoring & Log Management",
        "Troubleshooting & Maintenance"
    ],
    "Infrastructure Engineer": [
        "Server Hardware & Virtualization (VMware/KVM)",
        "Storage Systems (SAN/NAS/RAID)",
        "High Availability & Load Balancing",
        "Data Center Infrastructure & Networking",
        "Disaster Recovery & Backup Solutions",
        "Infrastructure Automation & Scripting"
    ],
    "Cyber Security Analyst": [
        "Information Security Fundamentals",
        "Threat Analysis & Vulnerability Assessment",
        "SIEM & Log Monitoring (Splunk)",
        "Network Security & Intrusion Detection",
        "Incident Response & Forensics",
        "Security Standards (ISO 27001/NIST)"
    ],
    "SOC Analyst": [
        "Security Event Monitoring & Triage",
        "SIEM Tools (Splunk/ELK)",
        "Packet Analysis & Wireshark",
        "Threat Intelligence & IOCs",
        "Incident Response Handling",
        "Malware Analysis Basics"
    ],
    "DevOps / Cloud Engineer": [
        "Containerization (Docker & Microservices)",
        "Orchestration (Kubernetes Architecture)",
        "CI/CD Pipelines (Jenkins/GitHub Actions)",
        "Infrastructure as Code (Terraform)",
        "Cloud Services (AWS/GCP/Azure)",
        "Monitoring & Observability (Prometheus/Grafana)"
    ],
    "Site Reliability Engineer (SRE)": [
        "SLOs, SLIs & Error Budgets",
        "System Observability & Monitoring",
        "Incident Management & Postmortems",
        "Infrastructure Automation & Go/Python",
        "Capacity Planning & Performance Tuning",
        "Chaos Engineering & Resilience Testing"
    ],
    # BDA / DBDA Roles
    "Python Developer": [
        "Python Syntax, Data Structures & Control Flow",
        "Object-Oriented Programming (OOP) & Modules",
        "File I/O, Exception Handling & Package Management",
        "Functional Programming, Generators & Decorators",
        "Web Frameworks (Django / Flask / FastAPI)",
        "Database Integration (SQLAlchemy / PostgreSQL)"
    ],
    "Data Analyst": [
        "Exploratory Data Analysis (EDA) & Pandas",
        "SQL Data Extraction, Joins & Aggregations",
        "Data Cleaning, Imputation & Feature Scaling",
        "Statistical Modeling & Hypothesis Testing",
        "Data Visualization (Matplotlib, Seaborn, Tableau)",
        "Business Metrics & Analytical Thinking"
    ],
    "Business Intelligence Developer": [
        "Data Warehousing & Dimensional Modeling (Star/Snowflake)",
        "ETL / ELT Pipeline Architecture",
        "Advanced SQL & Analytical Queries",
        "BI Dashboard Design (Power BI / Tableau / Looker)",
        "Data Governance & Metadata Management",
        "KPI Metrics & Performance Reporting"
    ],
    "Data Engineer": [
        "Data Warehousing & Schema Design (Star/Snowflake)",
        "ETL Pipeline Architecture & Orchestration (Airflow)",
        "SQL Query Optimization & Data Modeling",
        "Big Data Processing (Spark, Hadoop, PySpark)",
        "NoSQL Databases & Distributed Storage",
        "Data Quality, Governance & Streaming (Kafka)"
    ],
    "Machine Learning Engineer": [
        "Feature Engineering & Data Preprocessing",
        "Supervised Learning Algorithms (Regression, Classification)",
        "Unsupervised Learning (Clustering, Dimensionality Reduction)",
        "Model Evaluation Metrics & Cross-Validation",
        "Hyperparameter Optimization & Regularization",
        "Model Deployment & Inference Pipelines (MLOps)"
    ],
    "Deep Learning Engineer": [
        "Neural Network Architectures (ANN, CNN, RNN)",
        "Optimization Algorithms (SGD, Adam) & Loss Functions",
        "Deep Learning Frameworks (PyTorch / TensorFlow)",
        "Transfer Learning & Computer Vision / Audio Models",
        "Sequence Modeling & Attention Mechanisms",
        "Hardware Acceleration & Model Quantization"
    ],
    "AI Engineer": [
        "Core AI Principles & Heuristic Search",
        "Machine & Deep Learning Pipeline Integration",
        "Natural Language Processing (NLP) & Vision",
        "AI Agent Systems & Reasoning Frameworks",
        "API Integration & Model Serving (FastAPI / Triton)",
        "Ethical AI, Bias Mitigation & Robustness"
    ],
    "AI / LLM Engineer": [
        "Large Language Models (LLMs) & Transformer Architecture",
        "Retrieval-Augmented Generation (RAG) Architecture",
        "Vector Databases (ChromaDB, FAISS, Pinecone)",
        "Prompt Engineering, Chain-of-Thought & Agentic Workflows",
        "Fine-Tuning Strategies (LoRA, QLoRA, PEFT)",
        "LLM Evaluation, Guardrails & Production Deployment"
    ],
    "NLP Engineer": [
        "Text Preprocessing, Tokenization & Lemmatization",
        "Word Embeddings (Word2Vec, GloVe, FastText)",
        "Transformer Architectures (BERT, RoBERTa, T5)",
        "Named Entity Recognition (NER) & Text Classification",
        "Sequence-to-Sequence Models & Text Generation",
        "Evaluation Metrics (ROUGE, BLEU, Perplexity)"
    ],
    "Big Data Developer": [
        "Hadoop Ecosystem (HDFS, MapReduce, YARN)",
        "Apache Spark Core & Spark SQL",
        "Distributed Computing & Partitioning Strategies",
        "NoSQL Integration (HBase, Cassandra, MongoDB)",
        "Real-Time Data Streaming (Kafka, Spark Streaming)",
        "Data Ingestion & Extraction (Sqoop, Flume)"
    ],
    "Spark / Hadoop Engineer": [
        "HDFS Architecture & Data Replication",
        "Spark RDDs, DataFrames & Datasets",
        "PySpark & Spark Optimization (Caching, Shuffling)",
        "YARN Resource Allocation & Cluster Tuning",
        "Spark Streaming & Delta Lake",
        "ETL Pipeline Build with Hadoop & Spark"
    ],
    "Data Warehouse Engineer": [
        "Data Warehouse Architecture (Kimball vs Inmon)",
        "Dimensional Modeling (Facts & Dimensions)",
        "Slowly Changing Dimensions (SCD Types 1, 2, 3)",
        "ETL Pipeline Design & Data Staging",
        "SQL Query Performance Tuning & Partitioning",
        "Cloud Warehousing (Snowflake / Redshift / BigQuery)"
    ],
    "MLOps Engineer": [
        "Model Versioning & Experiment Tracking (MLflow, DVC)",
        "Automated ML Pipelines (Kubeflow, Airflow)",
        "Model Registry & Deployment (FastAPI, Triton, Docker)",
        "Model Monitoring (Drift Detection, Performance Degrade)",
        "CI/CD for Machine Learning (GitHub Actions, GitLab)",
        "Cloud MLOps Infrastructure (AWS SageMaker / Vertex AI)"
    ],
    # Cyber Security Roles
    "Penetration Tester / Ethical Hacker": [
        "Reconnaissance & Footprinting (Nmap, Shodan)",
        "Vulnerability Scanning & Assessment (Nessus)",
        "Web Application Security (OWASP Top 10)",
        "Exploitation Frameworks (Metasploit)",
        "Privilege Escalation Techniques (Linux/Windows)",
        "Penetration Testing Reporting & Remediation"
    ],
    "Security Engineer": [
        "Security Architecture & Threat Modeling",
        "Cryptography & Public Key Infrastructure (PKI)",
        "Network Security & Firewall Rule Engineering",
        "Identity & Access Management (IAM)",
        "Application Security & Secure Code Review",
        "Security Compliance & Auditing"
    ],
    "Information Security Manager": [
        "Information Security Governance & Strategy",
        "Risk Assessment & Management Frameworks",
        "Compliance Standards (ISO 27001, SOC 2, GDPR)",
        "Security Policies, Standards & Procedures",
        "Incident Management & Business Continuity",
        "Vendor & Third-Party Risk Management"
    ],
    "Cloud Security Engineer": [
        "Cloud IAM & Security Policy Engineering",
        "Cloud Network Security (VPCs, Security Groups)",
        "Data Encryption in Transit & at Rest (KMS)",
        "Cloud Compliance & Posture Management (CSPM)",
        "Container & Kubernetes Security",
        "Cloud Incident Response & Audit Logging"
    ],
    # Cloud Computing Roles
    "Cloud Architect": [
        "Multi-Cloud Architecture & Design Patterns",
        "Cloud Networking & VPC Architecture",
        "Cloud Storage & Database Selection",
        "Cost Optimization & Resource Management",
        "High Availability & Fault Tolerance Design",
        "Cloud Governance & Migration Strategies"
    ],
    "Cloud Engineer (AWS / Azure / GCP)": [
        "Core Compute Services (EC2 / VMs / Compute Engine)",
        "Cloud Storage (S3 / Blob / Cloud Storage)",
        "Identity & Access Management (IAM)",
        "Infrastructure as Code (Terraform / CloudFormation)",
        "Cloud Networking (VPCs, Subnets, Gateways)",
        "Cloud Monitoring & Automation (CloudWatch)"
    ],
    "DevOps Engineer": [
        "Version Control (Git Branching & Merging)",
        "Continuous Integration (Jenkins / GitHub Actions)",
        "Containerization (Docker)",
        "Container Orchestration (Kubernetes)",
        "Infrastructure as Code (Ansible / Terraform)",
        "Logging & Monitoring (ELK / Prometheus)"
    ],
    "Kubernetes / Container Specialist": [
        "Docker Containerization & Image Optimization",
        "Kubernetes Architecture (Control Plane, Worker Nodes)",
        "K8s Manifests (Deployments, StatefulSets, Services)",
        "Helm Chart Package Management",
        "K8s Ingress, Service Mesh & Network Policies",
        "Cluster Monitoring & Troubleshooting"
    ],
    # DAC & Web Roles
    "Full Stack Developer": [
        "HTML5, CSS3, Responsive Design & Modern UI",
        "JavaScript (ES6+) & TypeScript Core Concepts",
        "Frontend Frameworks (React / Vue / Angular)",
        "Backend APIs & Server-Side Logic (Node / Express / Python)",
        "Database Management & ORM Integration (SQL & MongoDB)",
        "RESTful API Design, Authentication & Deployment"
    ],
    "Backend Engineer": [
        "RESTful & GraphQL API Architecture",
        "Server-Side Languages (Python / Node / Java / Go)",
        "Database Query Optimization & Indexing",
        "Caching Strategies (Redis / Memcached)",
        "Asynchronous Processing & Message Queues (Celery/Kafka)",
        "API Security, Rate Limiting & Microservices"
    ],
    "Frontend Engineer": [
        "Modern JavaScript (ES6+), DOM & Async Operations",
        "React Component Architecture & State Management",
        "CSS Systems (Flexbox, Grid, Tailwind, Styled Components)",
        "Single Page Application (SPA) Routing & Performance",
        "Web Vitals, Optimization & Browser Compatibility",
        "Frontend Testing (Jest, React Testing Library)"
    ],
    "Java Developer": [
        "Java Core (OOP, Collections, Multithreading, Streams)",
        "Spring Framework & Spring Boot Core",
        "RESTful Web Services with Spring MVC",
        "Data Persistence (JPA / Hibernate / JDBC)",
        "Microservices Architecture & Spring Cloud",
        "Build Tools & Testing (Maven, Gradle, JUnit)"
    ],
    "C++ Developer": [
        "C++ Core (Pointers, Memory Management, RAII)",
        "Object-Oriented Programming & Polymorphism",
        "Standard Template Library (STL) Containers & Algorithms",
        "Modern C++ Features (C++11/14/17/20)",
        "Multithreading & Concurrency Control",
        "Performance Optimization & Debugging (GDB / Valgrind)"
    ],
    "Software Testing Engineer": [
        "Software Testing Methodologies (Manual & Automated)",
        "Test Case Design, Execution & Defect Tracking",
        "Web Automation Testing (Selenium / Playwright)",
        "API Testing (Postman / REST Assured)",
        "Performance & Load Testing (JMeter)",
        "CI/CD Integration for Test Automation"
    ],
    "Database Administrator": [
        "Database Installation, Configuration & Tuning",
        "SQL Query Performance Tuning & Execution Plans",
        "Database Backup, Recovery & Disaster Planning",
        "User Security, Roles & Privilege Management",
        "High Availability, Replication & Clustering",
        "Database Monitoring & Maintenance"
    ],
    "Web Developer": [
        "Semantic HTML5 & Modern CSS Layouts",
        "JavaScript DOM Manipulation & Event Handling",
        "Responsive Web Design & Cross-Browser Testing",
        "CMS Customization & Web Server Config (Nginx/Apache)",
        "Web Performance Optimization & SEO Basics",
        "Git Version Control & Deployment"
    ],
    # DMC Mobile Roles
    "Android App Developer": [
        "Kotlin Core & Object-Oriented Design",
        "Android Jetpack Architecture (ViewModel, LiveData, Room)",
        "UI Layouts & Jetpack Compose",
        "REST API Integration (Retrofit / Coroutines)",
        "App State Management & Background Services",
        "Play Store Publishing & App Optimization"
    ],
    "iOS App Developer": [
        "Swift Programming Language Core",
        "SwiftUI & UIKit Frameworks",
        "iOS App Architecture (MVVM / VIPER)",
        "Core Data & Local Persistence",
        "Networking & REST APIs (URLSession / Codable)",
        "App Store Guidelines & Deployment"
    ],
    "Flutter Developer": [
        "Dart Programming Language Concepts",
        "Flutter Widget Tree & UI Layouts",
        "State Management (Provider, Riverpod, BLoC)",
        "REST API & Firebase Integration",
        "Native Device Feature Integration (Plugins)",
        "Cross-Platform Deployment (Android & iOS)"
    ],
    "Cross-Platform Mobile Engineer": [
        "React Native / Flutter Framework Architecture",
        "Cross-Platform UI Components & Styling",
        "Native Bridge & Platform Channel Integration",
        "Mobile App State & Storage Management",
        "Performance Optimization & Memory Management",
        "CI/CD Pipelines for Mobile (Fastlane / Bitrise)"
    ],
    "Mobile UI/UX Architect": [
        "Mobile First UI/UX Design Principles",
        "Design Systems & Component Libraries",
        "User Journey Mapping & Wireframing",
        "Accessibility Standards (WCAG) for Mobile",
        "Animation & Interactive UI Micro-interactions",
        "Usability Testing & Feedback Iteration"
    ],
    # DESD Embedded Roles
    "Embedded Systems Engineer": [
        "Embedded C & Microcontroller Architecture",
        "Peripherals & Protocols (GPIO, UART, SPI, I2C, ADC)",
        "Hardware Abstraction Layer (HAL) & Drivers",
        "Interrupt Handling & Timers",
        "Memory Management & Pointer Manipulation",
        "Debugging & Instrumentation (Oscilloscope, Logic Analyzer)"
    ],
    "Firmware Engineer": [
        "Firmware Design Patterns & Bare-Metal Programming",
        "Bootloader Development & Firmware Update (OTA)",
        "Low-Power Mode & Energy Management",
        "Board Support Packages (BSP)",
        "Firmware Testing, Simulation & Validation",
        "Version Control & Release Engineering for Hardware"
    ],
    "IoT Developer": [
        "IoT Protocols (MQTT, CoAP, HTTP, WebSockets)",
        "Wireless Technologies (Wi-Fi, BLE, Zigbee, LoRaWAN)",
        "IoT Gateway Architecture & Edge Computing",
        "Cloud IoT Platform Integration (AWS IoT / Azure IoT)",
        "IoT Security & Device Authentication",
        "Sensor Integration & Signal Processing"
    ],
    "RTOS Engineer": [
        "Real-Time Operating System Concepts (FreeRTOS / Zephyr)",
        "Task Management, Scheduling & Priorities",
        "Inter-Task Communication (Queues, Semaphores, Mutexes)",
        "Memory Management & Stack Allocation in RTOS",
        "Interrupt Management & Context Switching",
        "Deterministic Execution & Timing Analysis"
    ],
    "Microcontroller Programmer": [
        "8/16/32-bit Microcontroller Architectures (ARM Cortex-M, AVR, PIC)",
        "Register-Level Programming & Bitwise Operations",
        "Peripheral Interfacing (LCD, Sensors, Motors)",
        "Clock Configuration & Power Domains",
        "Embedded C/C++ Optimization",
        "In-Circuit Emulation & Hardware Debugging"
    ],
    "Automotive Embedded Engineer": [
        "Automotive Protocols (CAN, LIN, FlexRay, Ethernet)",
        "AUTOSAR Architecture Standard",
        "ISO 26262 Functional Safety",
        "Model-Based Development (MATLAB / Simulink)",
        "ECU Software Development & Diagnostics (UDS)",
        "Hardware-in-the-Loop (HIL) Testing"
    ]
}

ALL_SUPPORTED_ROLES = sorted(list(ROLE_BLUEPRINTS.keys()))

def get_role_blueprint(role):
    """Returns the ordered topic blueprint array for a specified engineering role."""
    if role in ROLE_BLUEPRINTS:
        return ROLE_BLUEPRINTS[role]
    return [
        "Core Technical Fundamentals",
        "Practical Problem Solving",
        "System Architecture & Design",
        "Advanced Optimization & Debugging"
    ]

def get_all_roles():
    """Returns a sorted list of all supported engineering roles."""
    return ALL_SUPPORTED_ROLES

def predict_role_from_skills(skills):
    """
    Analyzes a list of extracted skills and returns the best matching target Role
    based on domain keyword weights, exact word-boundary matching, and blueprint topics.
    """
    if not skills:
        return "Linux System Administrator"

    skills_clean = [s.strip().lower() for s in skills if s.strip()]

    role_scores = {role: 0 for role in ROLE_BLUEPRINTS.keys()}

    for role, blueprint in ROLE_BLUEPRINTS.items():
        score = 0
        role_lower = role.lower()

        # 1. High Weight: Explicit Role-Specific Domain Keywords
        specific_keywords = ROLE_KEYWORD_WEIGHTS.get(role, [])
        for skill in skills_clean:
            for kw in specific_keywords:
                pattern = r'(?:\b|_)' + re.escape(kw) + r'(?:\b|_)'
                if re.search(pattern, skill) or skill == kw:
                    score += 10

        # 2. Medium Weight: Direct Role Title Word Boundary Matching
        for skill in skills_clean:
            if len(skill) <= 2 and skill in ["c", "r"]:
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, role_lower):
                    score += 6
            else:
                pattern = r'(?:\b|_)' + re.escape(skill) + r'(?:\b|_)'
                if re.search(pattern, role_lower):
                    score += 6

        # 3. Topic Blueprint Word Boundary Matching
        for topic in blueprint:
            words = [w.lower() for w in re.findall(r'\b[a-zA-Z]{3,}\b', topic)]
            for skill in skills_clean:
                if len(skill) <= 2:
                    continue
                if any(skill == w or (len(skill) > 3 and skill in w) for w in words):
                    score += 2

        role_scores[role] = score

    best_role = max(role_scores, key=role_scores.get)
    if role_scores[best_role] == 0:
        return "Python Developer"

    return best_role


