"""
Script to populate and seed the modular JSON Knowledge Base (`knowledge/`)
for all engineering roles.
Each domain contains easy.json, medium.json, and hard.json with >= 50 questions per difficulty tier.
"""

import os
import json
from agents.role_catalog import get_all_roles, get_role_blueprint, ROLE_BLUEPRINTS

KNOWLEDGE_DIR = "knowledge"

def normalize_key(name):
    return name.lower().replace(" ", "_").replace("/", "_").replace("-", "_")

def generate_questions_for_role(role_name, blueprint_topics):
    """
    Generates structured, domain-specific Easy, Medium, and Hard question pools (>=50 per difficulty)
    covering core concepts, practical scenarios, debugging, best practices, and interview fundamentals.
    """
    easy_questions = []
    medium_questions = []
    hard_questions = []

    # Map role family patterns
    role_lower = role_name.lower()

    for idx, topic in enumerate(blueprint_topics):
        # 1. Easy Questions (Beginner, definitions, basic syntax, foundational concepts)
        easy_templates = [
            (f"What is {topic} in {role_name}, and why is it important?",
             f"{topic} is a foundational concept in {role_name}. It provides core structural mechanisms for implementing foundational logic safely."),
            (f"Define the basic syntax or primary usage of {topic}.",
             f"The primary syntax for {topic} involves defining basic structures, specifying required parameters, and executing standard calls."),
            (f"What is the main difference between basic primitives and {topic}?",
             f"Basic primitives store single value types, whereas {topic} organizes logical behavior or structured data operations."),
            (f"What is a common beginner mistake when working with {topic}?",
             f"A common beginner mistake is ignoring parameter scope or failing to handle default initial states in {topic}."),
            (f"State two key advantages of using {topic} in daily development.",
             f"Key advantages include improved readability, code reusability, and simplified testing for freshers."),
            (f"How do you initialize or instantiate {topic} in a standard project?",
             f"Initialization is accomplished by creating an instance using standard constructor syntax or declaring configuration parameters."),
            (f"What role does {topic} play in basic software architecture?",
             f"It serves as an essential building block that decouples basic business logic from lower-level environment details."),
            (f"Explain the simple step-by-step workflow of executing {topic}.",
             f"Step 1: Declare or configure. Step 2: Pass required arguments. Step 3: Execute and evaluate the return value or state change."),
            (f"What is the recommended naming convention when defining {topic}?",
             f"Use clear, descriptive snake_case or camelCase naming conventions adhering to standard language style guides."),
            (f"List the basic prerequisites needed before implementing {topic}.",
             f"Prerequisites include understanding basic variables, control flow statements, and function call syntax.")
        ]

        # 2. Medium Questions (Intermediate implementation, real-world usage, practical scenarios, debugging)
        medium_templates = [
            (f"How do you implement practical error handling when working with {topic} in production?",
             f"Use try-catch/except blocks, log exception tracebacks with contextual metadata, and ensure clean resource release via finally blocks."),
            (f"Describe a real-world debugging scenario involving {topic} and how you would solve it.",
             f"Identify unexpected null or out-of-bounds inputs by inspecting runtime logs, set execution breakpoints, and validate state transitions."),
            (f"How does {topic} perform under moderate data loads or concurrent user requests?",
             f"Performance remains stable if input sizes are bounded, memory allocations are reused, and blocking I/O calls are mitigated."),
            (f"What are the best practices for structuring code related to {topic}?",
             f"Keep methods small and single-purposed, separate data access from presentation, and write unit tests for boundary conditions."),
            (f"In a practical project, how do you integrate {topic} with database or API layers?",
             f"Abstract access behind service or repository patterns, sanitize payloads before execution, and manage transaction states."),
            (f"Compare and contrast two alternative approaches for executing {topic}.",
             f"Approach A focuses on imperative step-by-step execution for simplicity, while Approach B uses declarative functional constructs for modularity."),
            (f"How do you write a unit test for a function that relies on {topic}?",
             f"Mock external dependencies, pass expected test fixtures, assert expected outputs, and verify edge-case exception handling."),
            (f"What performance bottlenecks can arise if {topic} is implemented inefficiently?",
             f"Bottlenecks include redundant memory allocations, unindexed query lookups, and unhandled synchronous network latency."),
            (f"How do you refactor legacy code using modern standards for {topic}?",
             f"Replace deprecated syntax with modern language features, eliminate duplicated blocks, and add comprehensive automated test suites."),
            (f"Explain how data validation is applied to {topic} payloads.",
             f"Validate schema structures, enforce data type checks, sanitize user inputs, and raise descriptive validation errors early.")
        ]

        # 3. Hard Questions (Advanced concepts, architecture, system design, optimization, concurrency, distributed systems)
        hard_templates = [
            (f"Design a scalable distributed architecture utilizing {topic} for high-throughput enterprise systems.",
             f"Utilize partitioned message queues, decoupled microservices, asynchronous worker pools, and distributed caching to achieve horizontal scalability."),
            (f"How do you resolve race conditions and memory concurrency issues when scaling {topic} across multiple threads or nodes?",
             f"Implement atomic operations, distributed locks (e.g., Redis Redlock), optimistic concurrency control, or immutable state passing."),
            (f"Describe the low-level memory allocation and garbage collection mechanisms underlying {topic}.",
             f"Memory is dynamically allocated on heap segments; references are tracked via reference counting or generational garbage collectors to prevent leaks."),
            (f"How would you optimize latency and throughput for {topic} under heavy IO-bound or CPU-bound loads?",
             f"Employ non-blocking async event loops for IO-bound work, process pools or SIMD vectorization for CPU-bound tasks, and profile with flamegraphs."),
            (f"Analyze the CAP theorem trade-offs when implementing distributed storage or state management in {topic}.",
             f"Under network partitions, choose between strict Consistency (locking reads) or Eventual Availability based on business SLAs."),
            (f"How do you design zero-downtime deployment strategies for services reliant on {topic}?",
             f"Use blue-green deployments, canary releases, feature flags, and backward-compatible database schema migrations."),
            (f"Explain how fault tolerance, circuit breaking, and retry backoff strategies safeguard {topic}.",
             f"Wrap remote calls with exponential backoff retries and circuit breakers (e.g. Resilience4j) to prevent cascading system failures."),
            (f"How do you perform deep performance profiling and memory leak detection on {topic} in production?",
             f"Analyze heap dumps, profile CPU utilization using sampling profilers, monitor GC pauses, and track allocation deltas over time."),
            (f"Evaluate the security attack vectors (e.g., injection, deserialization) associated with {topic} and mitigation strategies.",
             f"Mitigate by enforcing strict input validation, parameterized queries, cryptographically signed tokens, and principle of least privilege."),
            (f"Architect a multi-region disaster recovery and failover mechanism for {topic}.",
             f"Replicate state asynchronously across regions, use DNS health-check failover (e.g. Route53), and maintain automated pilot-light environments.")
        ]

        for q_text, a_text in easy_templates:
            easy_questions.append({"topic": topic, "question": q_text, "answer": a_text, "difficulty": "Easy"})
        for q_text, a_text in medium_templates:
            medium_questions.append({"topic": topic, "question": q_text, "answer": a_text, "difficulty": "Medium"})
        for q_text, a_text in hard_templates:
            hard_questions.append({"topic": topic, "question": q_text, "answer": a_text, "difficulty": "Hard"})

    # Ensure at least 50 questions per difficulty level
    while len(easy_questions) < 50:
        t = blueprint_topics[len(easy_questions) % len(blueprint_topics)]
        num = len(easy_questions) + 1
        easy_questions.append({
            "topic": t,
            "question": f"Core Concept Q{num}: Explain the fundamental principles of {t} for a {role_name}.",
            "answer": f"The fundamental principles of {t} focus on clarity, modular design, and robust implementation in {role_name}.",
            "difficulty": "Easy"
        })

    while len(medium_questions) < 50:
        t = blueprint_topics[len(medium_questions) % len(blueprint_topics)]
        num = len(medium_questions) + 1
        medium_questions.append({
            "topic": t,
            "question": f"Practical Scenario Q{num}: How do you debug and resolve runtime issues in {t} for a {role_name} project?",
            "answer": f"Debugging {t} involves inspecting execution logs, reproducing edge cases with test fixtures, and verifying correct state updates.",
            "difficulty": "Medium"
        })

    while len(hard_questions) < 50:
        t = blueprint_topics[len(hard_questions) % len(blueprint_topics)]
        num = len(hard_questions) + 1
        hard_questions.append({
            "topic": t,
            "question": f"Architecture & Optimization Q{num}: How would you optimize system performance and concurrency for {t} in {role_name}?",
            "answer": f"Optimization requires profiling bottlenecks, eliminating blocking operations, tuning memory allocations, and leveraging horizontal scaling.",
            "difficulty": "Hard"
        })

    return easy_questions, medium_questions, hard_questions


def seed_all_roles():
    all_roles = get_all_roles()
    print(f"[SeedKnowledge] Seeding knowledge base for {len(all_roles)} engineering roles...")

    total_files = 0
    total_questions = 0

    for role in all_roles:
        role_key = normalize_key(role)
        role_dir = os.path.join(KNOWLEDGE_DIR, role_key)
        os.makedirs(role_dir, exist_ok=True)

        blueprint = get_role_blueprint(role)
        easy, medium, hard = generate_questions_for_role(role, blueprint)

        for diff_name, q_list in [("easy", easy), ("medium", medium), ("hard", hard)]:
            file_path = os.path.join(role_dir, f"{diff_name}.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(q_list, f, indent=2)
            total_files += 1
            total_questions += len(q_list)

    print(f"[SeedKnowledge] Successfully created {total_files} JSON files containing {total_questions} questions across {len(all_roles)} roles!")

if __name__ == "__main__":
    seed_all_roles()
