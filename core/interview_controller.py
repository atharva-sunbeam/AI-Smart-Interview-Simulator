import os
import json
from typing import Dict, Any, List, Optional
from core.interview_state import InterviewState
from core.llm_factory import LLMFactory
from langchain_layer.interviewer_agent import LangChainInterviewerService
from crew_layer.interview_crew import InterviewCrewOrchestrator
from agents.role_catalog import get_role_blueprint
from rag_pipeline.rag import RAGPipeline


class InterviewController:
    """
    Central Controller for the AI Smart Interview Simulator.
    Wires Streamlit UI to:
    1. Centralized `InterviewState` model
    2. `InterviewCrewOrchestrator` (CrewAI: Agent -> Task -> Crew -> Process.sequential -> kickoff)
    3. `LangChainInterviewerService` (LangChain: create_agent -> @tool invocation -> Pydantic structured output)
    4. Underlying RAG DB & Knowledge Base
    """
    def __init__(self, state: Optional[InterviewState] = None):
        self.state = state or InterviewState()
        self.llm_factory = LLMFactory()
        self.langchain_service = LangChainInterviewerService(self.llm_factory)
        self.crew_orchestrator = InterviewCrewOrchestrator(self.llm_factory)
        self.rag_pipeline = RAGPipeline()
        self.rag_pipeline.initialize_db(force_recreate=False)

    def initialize_session(self, role: str, difficulty: str, count: int = 6, persona: str = "Alex", auto_speak: bool = True, resume_context: Optional[Dict[str, Any]] = None):
        """Initialize or reset interview session state."""
        self.state.target_role = role
        self.state.difficulty = difficulty
        self.state.main_question_count = count
        self.state.total_questions_target = count
        self.state.main_questions_asked = 0
        self.state.follow_up_count = 0
        self.state.interviewer_persona = persona
        self.state.auto_speak = auto_speak
        self.state.current_question_index = 0
        self.state.transcript.clear()
        self.state.asked_questions.clear()
        self.state.evaluations.clear()
        self.state.previous_evaluation = None
        self.state.interview_decisions.clear()
        self.state.debug_logs.clear()
        self.state.final_report = ""

        if resume_context:
            self.state.resume_context = resume_context

        self.state.add_debug_entry(
            component="Controller",
            action="Session Initialized",
            details={
                "role": role,
                "difficulty": difficulty,
                "count": count,
                "persona": persona,
                "has_resume": bool(resume_context and resume_context.get("skills"))
            }
        )

    def get_interview_blueprint(self) -> List[str]:
        """Creates dynamic interview blueprint matching candidate role, skills, and projects."""
        raw_blueprint = get_role_blueprint(self.state.target_role)
        skills = self.state.resume_context.get("skills", [])
        projects = self.state.resume_context.get("projects", [])

        if skills:
            skills_flat = [s.lower() for s in skills]
            prioritized = []
            remaining = []
            for topic in raw_blueprint:
                topic_lower = topic.lower()
                if any(s in topic_lower or topic_lower in s for s in skills_flat):
                    prioritized.append(topic)
                else:
                    remaining.append(topic)
            blueprint = prioritized + remaining
        else:
            blueprint = list(raw_blueprint)

        if self.state.total_questions_target > 5 and projects:
            num_project_q = 1 if self.state.total_questions_target <= 7 else 2
            project_topic = "Candidate Resume Project & Real-World Experience"
            if num_project_q >= 1 and len(blueprint) >= 3:
                blueprint.insert(3, project_topic)
            if num_project_q >= 2 and len(blueprint) >= 6:
                blueprint.insert(6, project_topic)

        return blueprint

    def generate_next_question(self) -> Dict[str, Any]:
        """
        Generates next adaptive question by orchestrating CrewAI tasks and LangChain tools.
        """
        blueprint = self.get_interview_blueprint()
        idx = self.state.current_question_index
        topic = blueprint[idx % len(blueprint)]
        self.state.current_topic = topic
        self.state.in_followup = False

        # 1. Execute CrewAI Question Strategy Task (Crew.kickoff)
        crew_res = self.crew_orchestrator.run_question_strategy_crew(
            role=self.state.target_role,
            difficulty=self.state.difficulty,
            topic=topic,
            previous_evaluation=self.state.previous_evaluation,
            resume_context=self.state.resume_context,
            state_logger=self.state
        )

        # 2. Execute LangChain Agent Reasoning & Tools (@tool invocation + create_agent)
        decision = self.langchain_service.generate_next_interview_decision(
            role=self.state.target_role,
            difficulty=self.state.difficulty,
            topic=topic,
            past_questions=self.state.asked_questions,
            previous_evaluation=self.state.previous_evaluation,
            resume_context=self.state.resume_context,
            state_logger=self.state
        )

        q_text = decision.next_question
        exp_ans = decision.expected_answer

        self.state.current_question = q_text
        self.state.current_expected_answer = exp_ans
        self.state.asked_questions.append(q_text)
        self.state.main_questions_asked += 1

        # Add to transcript
        self.state.add_transcript_turn(
            role="interviewer",
            message=q_text,
            metadata={"topic": topic, "difficulty": self.state.difficulty, "question_index": idx}
        )

        self.state.add_debug_entry(
            component="Controller",
            action="Generated Next Question",
            details={
                "question": q_text,
                "topic": topic,
                "difficulty": self.state.difficulty,
                "decision_action": decision.action,
                "reasoning": decision.reasoning_summary
            }
        )

        return {
            "question": q_text,
            "raw_question": q_text,
            "expected_answer": exp_ans,
            "topic": topic,
            "difficulty": self.state.difficulty
        }

    def evaluate_candidate_answer(self, user_answer: str) -> Dict[str, Any]:
        """
        Evaluates candidate response using CrewAI Answer Evaluation Task and LangChain `@tool`.
        """
        self.state.add_transcript_turn(
            role="candidate",
            message=user_answer,
            metadata={"question": self.state.current_question}
        )

        # 1. Execute CrewAI Evaluation Task
        crew_eval_str = self.crew_orchestrator.run_answer_evaluation_crew(
            question=self.state.current_question,
            expected_answer=self.state.current_expected_answer,
            user_answer=user_answer,
            state_logger=self.state
        )

        # 2. Execute LangChain evaluation tool & schema parsing
        structured_eval = self.langchain_service.evaluate_candidate_answer(
            question=self.state.current_question,
            expected_answer=self.state.current_expected_answer,
            user_answer=user_answer,
            state_logger=self.state
        )

        eval_dict = {
            "question": self.state.current_question,
            "topic": self.state.current_topic,
            "score": structured_eval.overall_score,
            "technical_score": structured_eval.technical_score,
            "relevance_score": structured_eval.relevance_score,
            "completeness_score": structured_eval.completeness_score,
            "clarity_score": structured_eval.clarity_score,
            "depth_score": structured_eval.depth_score,
            "overall_score": structured_eval.overall_score,
            "user_answer": user_answer,
            "feedback": structured_eval.feedback,
            "strengths": structured_eval.strengths,
            "weaknesses": structured_eval.weaknesses,
            "missing_concepts": structured_eval.missing_concepts,
            "incorrect_points": structured_eval.incorrect_points,
            "recommended_follow_up": structured_eval.recommended_follow_up,
            "follow_up_needed": structured_eval.follow_up_needed,
            "is_followup": self.state.in_followup
        }

        self.state.evaluations.append(eval_dict)
        self.state.previous_evaluation = eval_dict

        self.state.add_debug_entry(
            component="Controller",
            action="Evaluated Answer",
            details={
                "overall_score": structured_eval.overall_score,
                "technical_score": structured_eval.technical_score,
                "missing_concepts": structured_eval.missing_concepts,
                "follow_up_needed": structured_eval.follow_up_needed
            }
        )

        return eval_dict

    def generate_followup_question(self, user_answer: str) -> str:
        """Generates real-time adaptive probing question for missing concepts grounded strictly in candidate response."""
        self.state.in_followup = True
        self.state.follow_up_count += 1
        
        missing = []
        rec_fu = None
        if self.state.previous_evaluation:
            missing = self.state.previous_evaluation.get("missing_concepts", [])
            rec_fu = self.state.previous_evaluation.get("recommended_follow_up")

        # Clean parenthetical tool lists from topic string
        import re
        clean_topic = re.sub(r'\s*\([^)]*\)', '', self.state.current_topic).strip()

        # Extract concise snippet of candidate's actual response to ground follow-up
        ans_snippet = user_answer.strip()
        if len(ans_snippet) > 55:
            ans_snippet = ans_snippet[:52] + "..."

        if rec_fu and "earlier" not in rec_fu:
            followup = rec_fu
        elif missing:
            target_concept = missing[0]
            followup = f"You mentioned that '{ans_snippet}'. Can you explain how the system handles {target_concept} during retrieval?"
        else:
            followup = f"You explained that '{ans_snippet}'. Can you elaborate on the practical engineering trade-offs or failure modes of that approach in production?"

        self.state.followup_question = followup
        self.state.current_question = followup

        self.state.add_transcript_turn(
            role="interviewer",
            message=followup,
            metadata={"is_followup": True, "topic": clean_topic}
        )

        self.state.add_debug_entry(
            component="Controller",
            action="Generated Adaptive Follow-up",
            details={"followup": followup, "targeted_concept": missing[0] if missing else "general"}
        )

        return followup

    def generate_final_report(self) -> str:
        """Generates final report via CrewAI Final Report Task and updates self-learning database."""
        evals = self.state.evaluations
        total_evals = len(evals)

        if total_evals == 0:
            fallback_report = f"# Technical Interview Evaluation Report\n\n## Executive Summary\nNo questions evaluated in this session."
            self.state.final_report = fallback_report
            return fallback_report

        history_summary = ""
        total_score_sum = 0.0
        topic_scores = {}

        for i, ev in enumerate(evals):
            q_type = "Follow-up" if ev.get("is_followup") else "Main Q"
            score = ev.get("overall_score", ev.get("score", 5.0))
            total_score_sum += score
            topic = ev.get("topic", "General")
            if topic not in topic_scores:
                topic_scores[topic] = []
            topic_scores[topic].append(score)

            history_summary += f"Q{i+1} ({q_type}) [{topic}]: {ev.get('question')}\nAnswer: {ev.get('user_answer')}\nScore: {score}/10\nFeedback: {ev.get('feedback')}\n\n"

        avg_score = round(total_score_sum / total_evals, 1)

        # 1. Execute CrewAI Final Report Task
        crew_report = self.crew_orchestrator.run_final_report_crew(
            role=self.state.target_role,
            history_summary=history_summary,
            state_logger=self.state
        )

        # 2. Build structured markdown report if crew output is short/fallback
        if crew_report and len(crew_report.strip()) > 200 and "Executive Summary" in crew_report:
            if "# Technical Interview Evaluation Report" not in crew_report:
                final_report_text = "# Technical Interview Evaluation Report\n\n" + crew_report
            else:
                final_report_text = crew_report
        else:
            status = "Strong Hire" if avg_score >= 8.0 else ("Hire" if avg_score >= 6.0 else "Needs Preparation")
            
            report_md = f"# Technical Interview Evaluation Report\n\n"
            report_md += f"## Executive Summary\n"
            report_md += f"The candidate completed a structured technical interview for **{self.state.target_role}** (Difficulty: **{self.state.difficulty}**).\n"
            report_md += f"- **Questions Evaluated**: {total_evals}\n"
            report_md += f"- **Overall Performance Score**: **{avg_score} / 10**\n"
            report_md += f"- **Hiring Recommendation**: **{status}**\n\n"

            report_md += f"## Topic-wise Breakdown\n\n"
            report_md += f"| Technical Domain / Topic | Average Score | Status |\n"
            report_md += f"|---|---|---|\n"
            for t_name, scores in topic_scores.items():
                t_avg = round(sum(scores) / len(scores), 1)
                t_rating = "Proficient" if t_avg >= 7.0 else ("Developing" if t_avg >= 5.0 else "Needs Work")
                report_md += f"| {t_name} | {t_avg} / 10 | {t_rating} |\n"
            report_md += f"\n"

            report_md += f"## Key Strengths & Technical Highlights\n"
            all_strengths = [s for ev in evals for s in ev.get("strengths", [])]
            if all_strengths:
                for st_item in list(dict.fromkeys(all_strengths))[:5]:
                    report_md += f"- {st_item}\n"
            else:
                report_md += f"- Basic conceptual understanding demonstrated during the session.\n"
            report_md += f"\n"

            report_md += f"## Areas for Technical Improvement\n"
            all_weaknesses = [w for ev in evals for w in ev.get("weaknesses", [])]
            all_missing = [m for ev in evals for m in ev.get("missing_concepts", [])]
            if all_weaknesses or all_missing:
                for w_item in list(dict.fromkeys(all_weaknesses + [f"Missed {m}" for m in all_missing]))[:5]:
                    report_md += f"- {w_item}\n"
            else:
                report_md += f"- Focus on expanding production architecture trade-off explanations.\n"
            report_md += f"\n"

            report_md += f"## Final Assessment & Next Steps\n"
            if avg_score >= 8.0:
                report_md += f"The candidate demonstrated strong domain knowledge and practical understanding. Recommended for senior engineering roles."
            elif avg_score >= 6.0:
                report_md += f"The candidate has a solid foundational understanding. Focus on deepening practical debugging and system architecture concepts."
            else:
                report_md += f"The candidate should review foundational definitions, system design principles, and missing keywords highlighted above."

            final_report_text = report_md

        self.state.final_report = final_report_text

        # 3. Self-learning save to Chroma DB & JSON memory
        try:
            high_quality = [e for e in evals if e.get("score", 0) >= 7.0 or e.get("overall_score", 0) >= 7.0]
            if high_quality:
                self.rag_pipeline.add_session_to_knowledge_base(self.state.target_role, high_quality)
                self.state.add_debug_entry(
                    component="RAG",
                    action="Continuous Learning",
                    details=f"Added {len(high_quality)} high-scoring Q&A pairs to Chroma DB vector store."
                )
        except Exception as e:
            print(f"[Controller Self Learning Warning] {e}")

        return self.state.final_report
