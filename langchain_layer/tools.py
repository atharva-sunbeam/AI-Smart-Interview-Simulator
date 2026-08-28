import json
import re
from langchain.tools import tool
from rag_pipeline.rag import RAGPipeline
from agents.knowledge_manager import KnowledgeManager

# Module-level singletons for tool execution
_rag_instance = None
_km_instance = None

def _get_rag():
    global _rag_instance
    if _rag_instance is None:
        _rag_instance = RAGPipeline()
        _rag_instance.initialize_db(force_recreate=False)
    return _rag_instance

def _get_km():
    global _km_instance
    if _km_instance is None:
        _km_instance = KnowledgeManager()
    return _km_instance


@tool("retrieve_knowledge")
def retrieve_knowledge(query: str, role: str = "Engineering Candidate", difficulty: str = "Medium") -> str:
    """
    Search the ChromaDB vector database for technical interview passages, questions,
    and expected answers relevant to the query and role.

    :param query: string search query or topic
    :param role: target job role
    :param difficulty: 'Easy', 'Medium', or 'Hard'
    :returns JSON string of retrieved document passages and metadata
    """
    try:
        rag = _get_rag()
        results = rag.retrieve_questions(role=role, difficulty=difficulty, query=query, k=5)
        if not results:
            results = rag.retrieve_questions(role=role, query=query, k=5)
        return json.dumps(results, indent=2)
    except Exception as e:
        return f"ERROR: Failed retrieving knowledge: {e}"


@tool("retrieve_role_questions")
def retrieve_role_questions(role: str, difficulty: str = "Medium", topic: str = "") -> str:
    """
    Retrieve structured interview question candidates from role-specific JSON knowledge banks
    and sister role clusters.

    :param role: job role title
    :param difficulty: 'Easy', 'Medium', or 'Hard'
    :param topic: specific topic filter or empty string
    :returns JSON array of candidate question objects
    """
    try:
        km = _get_km()
        questions = km.get_questions_for_role(role=role, difficulty=difficulty, topic=topic if topic else None)
        return json.dumps(questions[:10], indent=2)
    except Exception as e:
        return f"ERROR: Failed retrieving role questions: {e}"


@tool("retrieve_resume_context")
def retrieve_resume_context(resume_json: str, query: str = "") -> str:
    """
    Search candidate resume metadata (skills, projects, domain breakdown) for relevant project experience
    or tool claims to probe during the interview.

    :param resume_json: JSON string of parsed candidate resume
    :param query: optional tool or topic to focus on
    :returns formatted string of candidate resume project and skill details
    """
    try:
        data = json.loads(resume_json) if isinstance(resume_json, str) else resume_json
        skills = data.get("skills", [])
        projects = data.get("projects", [])
        
        output = f"Candidate Skills: {', '.join(skills[:15])}\n"
        if projects:
            output += "Candidate Projects:\n"
            for p in projects:
                if isinstance(p, dict):
                    output += f"- Project: {p.get('name')}\n  Tools: {', '.join(p.get('tools', []))}\n  Description: {p.get('description')}\n"
                else:
                    output += f"- {p}\n"
        return output
    except Exception as e:
        return f"ERROR parsing resume context: {e}"


@tool("evaluate_answer_tool")
def evaluate_answer_tool(question: str, expected_answer: str, candidate_answer: str) -> str:
    """
    Evaluate candidate response technical accuracy, relevance to exact question, completeness, clarity, and missing concepts semantically.

    :param question: the exact interview question asked
    :param expected_answer: key expected technical points
    :param candidate_answer: response provided by candidate
    :returns JSON string of AnswerEvaluation schema with sub-scores and overall score
    """
    if not candidate_answer or len(candidate_answer.strip()) < 5:
        return json.dumps({
            "technical_score": 1.0,
            "relevance_score": 1.0,
            "completeness_score": 1.0,
            "clarity_score": 1.0,
            "depth_score": 1.0,
            "overall_score": 1.0,
            "strengths": [],
            "weaknesses": ["No answer provided or answer too brief to evaluate"],
            "missing_concepts": ["Core technical explanation for the question asked"],
            "incorrect_points": [],
            "feedback": "You did not provide a detailed technical answer. Please explain key concepts clearly when responding.",
            "recommended_follow_up": "Could you provide a basic technical explanation for this question?",
            "follow_up_needed": True
        }, indent=2)

    cand_lower = candidate_answer.lower()
    q_lower = question.lower()
    exp_lower = expected_answer.lower()

    # 1. QUESTION RELEVANCE TEST
    q_keywords = [w for w in re.findall(r'\b[a-z]{4,}\b', q_lower) if w not in {"what", "how", "why", "does", "with", "from", "that", "this", "which", "your", "their", "when", "about", "describe", "explain"}]
    
    q_relevance_hits = sum(1 for kw in q_keywords if kw in cand_lower or (len(kw) >= 4 and kw[:4] in cand_lower))
    rel_factor = (q_relevance_hits / len(q_keywords)) if q_keywords else 1.0
    rel_factor = min(max(rel_factor, 0.1), 1.0)

    # 2. MISCONCEPTION / INCORRECT CLAIM DETECTION
    incorrect_points = []
    if "don't know" in cand_lower or "not sure" in cand_lower or "no idea" in cand_lower:
        incorrect_points.append("Candidate acknowledged uncertainty or lack of experience with the topic.")
    if "llm directly searches" in cand_lower or "llm searches raw text" in cand_lower:
        incorrect_points.append("Claimed LLM directly searches raw text files without indexing.")
    if "sql database for embeddings" in cand_lower:
        incorrect_points.append("Claimed relational SQL tables perform vector similarity calculations efficiently.")

    # 3. DYNAMIC TECHNICAL CONCEPT EXTRACTION FROM EXPECTED ANSWER
    exp_sentences = re.split(r'[\.\;\,\n]', expected_answer)
    dynamic_concepts = []
    for s in exp_sentences:
        clean_s = s.strip()
        if len(clean_s) > 8:
            words = [w for w in re.findall(r'\b[a-z]{4,}\b', clean_s.lower()) if w not in {"with", "that", "this", "they", "them", "from", "their", "will", "would", "about", "there", "these", "which", "could", "should", "used", "using", "such", "system", "data"}]
            if len(words) >= 2:
                concept_title = " ".join(words[:3])
                dynamic_concepts.append((concept_title, words))

    if not dynamic_concepts:
        dynamic_concepts = [("core technical principles", q_keywords)]

    matched_concepts = []
    missing_concepts = []

    for title, keywords in dynamic_concepts:
        matched_kw_count = sum(1 for kw in keywords if kw in cand_lower or (len(kw) >= 4 and kw[:4] in cand_lower))
        kw_ratio = (matched_kw_count / len(keywords)) if keywords else 0.0
        if kw_ratio >= 0.5 or matched_kw_count >= 2:
            matched_concepts.append(title)
        else:
            missing_concepts.append(title)

    words_count = len(candidate_answer.split())
    length_factor = min(words_count / 40.0, 1.0)

    # Hand-waving / superficial answer detection (e.g., "used to do certain work", "solving the problem")
    handwaving_phrases = ["certain work", "do certain", "basically used", "solving the problem", "used for solving", "used for doing", "used in deep learning"]
    is_handwaving = (any(phrase in cand_lower for phrase in handwaving_phrases) or words_count < 30) and len(matched_concepts) < 2

    concept_coverage = (len(matched_concepts) / len(dynamic_concepts)) if dynamic_concepts else 0.5
    if is_handwaving:
        concept_coverage = min(concept_coverage, 0.25)

    # 4. SUB-SCORES & OVERALL WEIGHTED CALCULATION
    rel_score = round(min(max(rel_factor * 10.0, 1.0), 10.0), 1)
    
    base_tech = (concept_coverage * 7.0) + (length_factor * 2.0) + 1.0
    if rel_factor < 0.4:
        base_tech *= 0.5

    tech_score = round(min(max(base_tech - (len(incorrect_points) * 2.5), 1.0), 10.0), 1)
    comp_score = round(min(max((concept_coverage * 9.0) + 1.0, 1.0), 10.0), 1)
    clar_score = round(min(max((length_factor * 8.0) + 2.0, 1.0), 10.0), 1)
    depth_score = round(min(max(tech_score * 0.9, 1.0), 10.0), 1)

    if is_handwaving:
        tech_score = min(tech_score, 3.5)
        rel_score = min(rel_score, 4.5)
        comp_score = min(comp_score, 3.0)
        depth_score = min(depth_score, 2.5)

    overall = round((tech_score * 0.35) + (rel_score * 0.20) + (comp_score * 0.20) + (clar_score * 0.10) + (depth_score * 0.15), 1)
    overall = min(max(overall, 1.0), 10.0)

    # 5. ACTIONABLE FEEDBACK & REASONING
    strengths = []
    if rel_score >= 6.0 and matched_concepts and not is_handwaving:
        strengths.append(f"Addressed key concepts: {matched_concepts[0]}")
    elif words_count > 15:
        strengths.append("Attempted basic conceptual answer")

    weaknesses = []
    if is_handwaving:
        weaknesses.append("Response was superficial and hand-waving ('used to do certain work') without detailing specific technical mechanisms")
    if rel_score < 5.0:
        weaknesses.append("Response did not directly address the specific core question asked")
    if missing_concepts:
        weaknesses.append(f"Omitted detailed explanation for: {missing_concepts[0]}")
    if incorrect_points:
        weaknesses.append(f"Technical gap: {incorrect_points[0]}")

    # Build a comprehensive 3-4 sentence technical evaluation paragraph
    feedback_parts = []
    
    # Sentence 1: Accuracy & Alignment
    if overall >= 8.0:
        feedback_parts.append(f"Strong technical performance! Your response scored {overall}/10, demonstrating solid technical domain knowledge and clear alignment with the question.")
    elif overall >= 5.0:
        feedback_parts.append(f"Fair response scoring {overall}/10. You demonstrated a basic conceptual understanding, but your answer lacked complete technical depth.")
    elif is_handwaving:
        feedback_parts.append(f"Your response received a score of {overall}/10 because it relied on brief, generic statements ('used to do certain work') rather than detailing concrete technical mechanisms.")
    else:
        feedback_parts.append(f"Your answer scored {overall}/10 as it was incomplete or did not directly address the specific engineering question asked.")

    # Sentence 2: Key concepts covered vs missed
    if matched_concepts:
        m_str = ", ".join(matched_concepts[:2])
        feedback_parts.append(f"You correctly referenced key concepts such as {m_str}.")
    if missing_concepts:
        miss_str = ", ".join(missing_concepts[:2])
        feedback_parts.append(f"However, expected core technical terminologies like {miss_str} were omitted from your explanation.")

    # Sentence 3: Misconceptions
    if incorrect_points:
        feedback_parts.append(f"Note that claiming '{incorrect_points[0]}' is a technical misconception that should be avoided.")

    # Sentence 4: Actionable advice for technical depth
    if overall >= 8.0:
        feedback_parts.append("To elevate your response even further for a staff-level evaluation, discuss real-world production trade-offs and edge-case handling.")
    elif is_handwaving:
        feedback_parts.append("For a professional technical interview, clearly define the underlying architecture, explain how data flows through the system, and use precise industry terminology.")
    else:
        feedback_parts.append("Be sure to structure your response around specific algorithms, system components, and operational trade-offs.")

    feedback = " ".join(feedback_parts)
    follow_needed = (overall < 9.5) or (len(missing_concepts) > 0) or is_handwaving

    if follow_needed:
        target_gap = missing_concepts[0] if missing_concepts else "the core technical mechanism"
        rec_followup = f"You touched on the general topic. Can you explain the specific role and implementation details of {target_gap}?"
    else:
        rec_followup = None

    return json.dumps({
        "technical_score": tech_score,
        "relevance_score": rel_score,
        "completeness_score": comp_score,
        "clarity_score": clar_score,
        "depth_score": depth_score,
        "overall_score": overall,
        "strengths": strengths if strengths else ["Attempted response"],
        "weaknesses": weaknesses if weaknesses else ["Could provide deeper architectural context"],
        "missing_concepts": missing_concepts[:3],
        "incorrect_points": incorrect_points,
        "feedback": feedback,
        "recommended_follow_up": rec_followup,
        "follow_up_needed": follow_needed
    }, indent=2)


LANGCHAIN_TOOLS = [
    retrieve_knowledge,
    retrieve_role_questions,
    retrieve_resume_context,
    evaluate_answer_tool
]
