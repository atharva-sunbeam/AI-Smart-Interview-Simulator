from crewai import Task


def create_question_generation_task(agent, role, difficulty, topic, previous_evaluation=None, resume_context=None):
    """CrewAI Task for Question Strategist Agent."""
    prev_info = f"Previous Evaluation: {previous_evaluation}\n" if previous_evaluation else "Previous Evaluation: None\n"
    res_info = f"Resume Details: {resume_context}\n" if resume_context else "Resume Details: None\n"

    description = (
        f"Design the next technical interview question for candidate interviewing for {role}.\n"
        f"Target Topic: {topic}\n"
        f"Strict Difficulty: {difficulty}\n"
        f"{prev_info}"
        f"{res_info}"
        f"Task:\n"
        f"1. Check if the candidate missed specific concepts in their previous answer. If so, generate an adaptive probing question.\n"
        f"2. If topic relates to resume projects, craft a deep-dive project implementation question.\n"
        f"3. Output the exact question text and key expected points."
    )
    expected_output = "JSON or structured text containing 'question', 'expected_answer', 'topic', and 'reasoning'."

    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent
    )


def create_answer_evaluation_task(agent, question, expected_answer, user_answer):
    """CrewAI Task for Answer Evaluator Agent."""
    description = (
        f"Evaluate candidate response objectively.\n"
        f"Question Asked: {question}\n"
        f"Expected Answer: {expected_answer}\n"
        f"Candidate Answer: {user_answer}\n\n"
        f"Task:\n"
        f"1. Score technical accuracy from 1 to 10.\n"
        f"2. Identify key strengths and exact missing technical concepts/keywords.\n"
        f"3. Provide constructive feedback."
    )
    expected_output = "Structured assessment detailing technical_score (1-10), strengths, missing_concepts, and feedback."

    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent
    )


def create_followup_decision_task(agent, question, user_answer, evaluation):
    """CrewAI Task for Interview Supervisor Agent."""
    description = (
        f"Review candidate answer evaluation and decide whether to issue a probing follow-up or proceed.\n"
        f"Main Question: {question}\n"
        f"Candidate Answer: {user_answer}\n"
        f"Evaluation: {evaluation}\n\n"
        f"Task: Generate a natural conversational follow-up question if technical score < 7.0 or if missing concepts exist."
    )
    expected_output = "Conversational follow-up question string or decision directive."

    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent
    )


def create_final_report_task(agent, role, history_summary):
    """CrewAI Task for Executive Performance Reporting."""
    description = (
        f"Compile executive performance report for candidate interviewing for {role}.\n"
        f"Session History Log:\n{history_summary}\n\n"
        f"Task: Generate markdown report with Executive Summary, Topic Breakdown Table, Key Strengths, Areas for Improvement, and Final Recommendation."
    )
    expected_output = "Complete structured Markdown report string."

    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent
    )
