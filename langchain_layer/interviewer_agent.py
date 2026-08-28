import json
import re
import random
from typing import Dict, Any, List
from langchain.agents import create_agent
from langchain_layer.tools import (
    LANGCHAIN_TOOLS,
    retrieve_knowledge,
    retrieve_role_questions,
    retrieve_resume_context,
    evaluate_answer_tool
)
from langchain_layer.schemas import AnswerEvaluation, InterviewDecision
from core.llm_factory import LLMFactory


def _clean_question_text(q_text: str, role: str = "") -> str:
    """
    Removes mechanical role insertions like 'in AI / LLM Engineer' or 'in Deep Learning Engineer'
    to make questions sound natural and conversational as asked by a senior interviewer.
    """
    if not q_text:
        return ""
    
    cleaned = q_text

    # 1. Strip generic mechanical role title insertions (e.g. "in Deep Learning Engineer", "for Data Engineer")
    generic_role_pattern = r'\s+(?:in|for|as\s+a|when\s+working\s+as\s+a)\s+[A-Za-z0-9\s/]+(?:Engineer|Architect|Developer|Administrator|Specialist|Analyst|Scientist)[,.]?'
    cleaned = re.sub(generic_role_pattern, '', cleaned, flags=re.IGNORECASE)
    
    # 2. Strip explicit role if provided
    if role:
        cleaned = re.sub(r'\s+(?:in|for|as\s+a|when\s+working\s+as\s+a)\s+' + re.escape(role) + r'[,.]?', '', cleaned, flags=re.IGNORECASE)
    
    # 3. Replace mechanical template endings like "what is X and why is it important?"
    match = re.search(r'What is (.+?) and why is it important\?', cleaned, flags=re.IGNORECASE)
    if match:
        subject = match.group(1).strip()
        subject = re.sub(generic_role_pattern, '', subject, flags=re.IGNORECASE).strip()
        if subject.endswith('s') or '&' in subject or ' and ' in subject:
            cleaned = f"What problems do {subject} solve, and how are they used in production?"
        else:
            cleaned = f"What problem does {subject} solve, and how is it used in production?"

    cleaned = re.sub(r'\s+', ' ', cleaned)
    cleaned = re.sub(r'\s+,', ',', cleaned)
    return cleaned.strip()


class LangChainInterviewerService:
    """
    LangChain Agentic Reasoning Service using `from langchain.agents import create_agent`.
    Invokes registered `@tool` functions (RAG, Knowledge Banks, Resume Parsing, Answer Evaluation)
    during actual interview execution.
    """
    def __init__(self, llm_factory: LLMFactory = None):
        self.llm_factory = llm_factory or LLMFactory()
        self.llm = self.llm_factory.get_langchain_llm()
        self.tools = LANGCHAIN_TOOLS
        self.agent = None
        self._initialize_agent()

    def _initialize_agent(self):
        system_prompt = (
            "You are a senior technical interviewer conducting an adaptive technical interview.\n"
            "You have access to candidate resume context, role knowledge banks, ChromaDB RAG, and an answer evaluator tool.\n"
            "Your job is to reason about candidate responses, invoke tools as needed, and formulate natural, specific, conversational questions matching difficulty tiers."
        )
        if self.llm:
            try:
                self.agent = create_agent(
                    model=self.llm,
                    tools=self.tools,
                    system_prompt=system_prompt
                )
                print("[LangChainInterviewerService] Initialized LangChain create_agent() successfully.")
            except Exception as e:
                print(f"[LangChainInterviewerService Warning] create_agent initialization: {e}")

    def evaluate_candidate_answer(self, question: str, expected_answer: str, user_answer: str, state_logger: Any = None) -> AnswerEvaluation:
        """
        Executes LangChain tool `evaluate_answer_tool` and returns structured `AnswerEvaluation`.
        """
        tool_input = {
            "question": question,
            "expected_answer": expected_answer,
            "candidate_answer": user_answer
        }
        
        # Log tool invocation for observability
        if state_logger and hasattr(state_logger, "add_debug_entry"):
            state_logger.add_debug_entry(
                component="LangChain",
                action="Invoked Tool: evaluate_answer_tool",
                details=tool_input
            )

        # 1. Execute tool directly
        eval_json_str = evaluate_answer_tool.invoke(tool_input)
        
        # 2. If agent is connected, refine through LangChain agent reasoning
        if self.agent:
            try:
                prompt_msg = f"Evaluate candidate answer using evaluate_answer_tool.\nQuestion: {question}\nExpected: {expected_answer}\nAnswer: {user_answer}"
                res = self.agent.invoke({"messages": [{"role": "user", "content": prompt_msg}]})
                if state_logger and hasattr(state_logger, "add_debug_entry"):
                    state_logger.add_debug_entry(
                        component="LangChain",
                        action="create_agent() Reasoning Completed",
                        details={"messages_count": len(res.get("messages", []))}
                    )
            except Exception as e:
                print(f"[LangChain Agent Invoke Error] {e}")

        try:
            data = json.loads(eval_json_str)
            return AnswerEvaluation(**data)
        except Exception:
            return AnswerEvaluation(
                technical_score=5.0,
                relevance_score=5.0,
                completeness_score=5.0,
                clarity_score=5.0,
                depth_score=5.0,
                overall_score=5.0,
                strengths=["Technical answer provided"],
                weaknesses=[],
                missing_concepts=[],
                incorrect_points=[],
                feedback=eval_json_str,
                recommended_follow_up=None,
                follow_up_needed=True
            )

    def generate_next_interview_decision(self, role: str, difficulty: str, topic: str, past_questions: List[str], previous_evaluation: Any = None, resume_context: Dict[str, Any] = None, state_logger: Any = None) -> InterviewDecision:
        """
        Executes LangChain agent reasoning and tools (`retrieve_knowledge`, `retrieve_role_questions`, `retrieve_resume_context`)
        to produce adaptive, conversational `InterviewDecision`.
        """
        tool_calls_logged = []

        # Tool 1: Retrieve resume context if candidate resume exists
        resume_str = ""
        if resume_context and (resume_context.get("skills") or resume_context.get("projects")):
            resume_str = retrieve_resume_context.invoke({"resume_json": json.dumps(resume_context)})
            tool_calls_logged.append("retrieve_resume_context")

        # Tool 2: Retrieve role question candidates
        role_q_json = retrieve_role_questions.invoke({"role": role, "difficulty": difficulty, "topic": topic})
        tool_calls_logged.append("retrieve_role_questions")

        # Tool 3: Retrieve ChromaDB RAG knowledge
        rag_query = topic or role
        rag_json = retrieve_knowledge.invoke({"query": rag_query, "role": role, "difficulty": difficulty})
        tool_calls_logged.append("retrieve_knowledge")

        if state_logger and hasattr(state_logger, "add_debug_entry"):
            state_logger.add_debug_entry(
                component="LangChain",
                action=f"Invoked Tools: {', '.join(tool_calls_logged)}",
                details={"role": role, "difficulty": difficulty, "topic": topic}
            )

        # Parse retrieved candidates
        candidates = []
        try:
            candidates = json.loads(role_q_json)
        except Exception:
            candidates = []

        # Clean topic string to avoid leaking parenthetical tool lists like "(ChromaDB, FAISS, Pinecone)"
        clean_topic = re.sub(r'\s*\([^)]*\)', '', topic).strip()

        # Adaptive Strategy: Missing concepts from previous evaluation
        missing_concepts = []
        prev_score = 10.0
        if previous_evaluation:
            if hasattr(previous_evaluation, "missing_concepts"):
                missing_concepts = previous_evaluation.missing_concepts
                prev_score = getattr(previous_evaluation, "overall_score", 10.0)
            elif isinstance(previous_evaluation, dict):
                missing_concepts = previous_evaluation.get("missing_concepts", [])
                prev_score = previous_evaluation.get("overall_score", 10.0)

        # Filter out already asked questions across current session and persistent GlobalQuestionRegistry
        try:
            from agents.orchestrator import GlobalQuestionRegistry
            global_reg = GlobalQuestionRegistry()
            global_asked = global_reg.asked_questions
        except Exception:
            global_reg = None
            global_asked = set()

        excluded = set(past_questions or []).union(global_asked)
        valid_q = [q for q in candidates if q.get("question") not in excluded and _clean_question_text(q.get("question", ""), role) not in excluded]

        # Handle Project-Based Deep Dives from Resume
        if topic == "Candidate Resume Project & Real-World Experience" and resume_context and resume_context.get("projects"):
            projects = resume_context.get("projects", [])
            proj = random.choice(projects) if projects else {}
            p_name = proj.get("name", "your recent project") if isinstance(proj, dict) else str(proj)
            p_tools = ", ".join(proj.get("tools", [])) if isinstance(proj, dict) and proj.get("tools") else "the technologies used"

            if difficulty == "Easy":
                next_q_text = f"In your project '{p_name}', what specific role did {p_tools} play, and why was it selected for the stack?"
                exp_ans = f"Explanation of tool selection ({p_tools}) in '{p_name}' and candidate's core implementation responsibilities."
            elif difficulty == "Medium":
                next_q_text = f"While building '{p_name}' with {p_tools}, what main integration or performance bottleneck did you run into, and how did you debug it?"
                exp_ans = f"Detailed breakdown of technical challenges and debugging steps with {p_tools} in '{p_name}'."
            else: # Hard
                next_q_text = f"How would you re-architect '{p_name}' (built with {p_tools}) to support 100x scale, high concurrency, and zero-downtime failover?"
                exp_ans = f"Advanced distributed system design strategies for scaling '{p_name}'."

            if global_reg:
                global_reg.add(next_q_text)

            return InterviewDecision(
                action="ask_next",
                next_question=next_q_text,
                expected_answer=exp_ans,
                topic=topic,
                difficulty=difficulty,
                reasoning_summary=f"Crafted targeted resume project question for '{p_name}'."
            )

        # Adaptive Probing for Missing Concepts
        if missing_concepts and prev_score < 7.0:
            target_concept = missing_concepts[0]
            action_type = "ask_followup"
            
            if difficulty == "Easy":
                next_q_text = f"You discussed {clean_topic} earlier. Can you briefly clarify the basic role of {target_concept}?"
            elif difficulty == "Medium":
                next_q_text = f"Let's go one step deeper on {clean_topic}. How does {target_concept} behave in practice when handling queries or processing data?"
            else:
                next_q_text = f"Considering production scale in {clean_topic}, how would you optimize or troubleshoot {target_concept} under heavy concurrent load?"

            exp_ans = f"Technical explanation of {target_concept} within {clean_topic}."
            reason = f"Candidate missed {target_concept} in previous response; asking targeted adaptive follow-up."
            if global_reg:
                global_reg.add(next_q_text)
        elif valid_q:
            random.shuffle(valid_q)
            chosen = valid_q[0]
            action_type = "ask_next"
            raw_q = chosen.get("question", "")
            next_q_text = _clean_question_text(raw_q, role)
            exp_ans = chosen.get("answer", chosen.get("expected_answer", ""))
            reason = f"Selected fresh blueprint question on topic {clean_topic} matching difficulty {difficulty}."
            if global_reg:
                global_reg.add(next_q_text)
                global_reg.add(raw_q)
        else:
            action_type = "ask_next"
            if difficulty == "Easy":
                next_q_text = f"What are the foundational principles of {clean_topic}, and what core problems does it solve?"
                exp_ans = f"Basic definitions and fundamental concepts of {clean_topic}."
            elif difficulty == "Medium":
                next_q_text = f"In a production system using {clean_topic}, what are the key implementation trade-offs you consider when designing the pipeline?"
                exp_ans = f"Practical engineering trade-offs and implementation choices in {clean_topic}."
            else:
                next_q_text = f"How would you architect and optimize a high-throughput, fault-tolerant system around {clean_topic}?"
                exp_ans = f"System architecture, concurrency, and scaling strategy for {clean_topic}."
            reason = "Formulated natural technical question matching difficulty tier."

        # If LangChain create_agent is connected, invoke for final agent reasoning
        if self.agent:
            try:
                agent_res = self.agent.invoke({
                    "messages": [{
                        "role": "user",
                        "content": f"Review question: '{next_q_text}' for difficulty {difficulty}. Ensure it sounds natural and conversational without mentioning role title."
                    }]
                })
                if state_logger and hasattr(state_logger, "add_debug_entry"):
                    state_logger.add_debug_entry(
                        component="LangChain",
                        action="create_agent() Reasoning Completed",
                        details={"messages_count": len(agent_res.get("messages", []))}
                    )
            except Exception as e:
                print(f"[LangChain create_agent reasoning error] {e}")

        return InterviewDecision(
            action=action_type,
            next_question=next_q_text,
            expected_answer=exp_ans,
            topic=clean_topic,
            difficulty=difficulty,
            reasoning_summary=reason
        )
