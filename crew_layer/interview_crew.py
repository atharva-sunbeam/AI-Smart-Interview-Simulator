import json
from typing import Dict, Any, Optional
from crewai import Crew, Process
from crew_layer.agents import create_interview_crew_agents
from crew_layer.tasks import (
    create_question_generation_task,
    create_answer_evaluation_task,
    create_followup_decision_task,
    create_final_report_task
)
from core.llm_factory import LLMFactory


class InterviewCrewOrchestrator:
    """
    CrewAI Orchestrator managing multi-agent workflow execution using:
    - Agent
    - Task
    - Crew
    - Process.sequential
    - crew.kickoff()
    """
    def __init__(self, llm_factory: LLMFactory = None):
        self.llm_factory = llm_factory or LLMFactory()
        self.agents_dict = create_interview_crew_agents(self.llm_factory)
        self.supervisor = self.agents_dict["supervisor"]
        self.strategist = self.agents_dict["strategist"]
        self.interviewer = self.agents_dict["interviewer"]
        self.evaluator = self.agents_dict["evaluator"]

    def run_question_strategy_crew(self, role: str, difficulty: str, topic: str, previous_evaluation: Any = None, resume_context: Dict[str, Any] = None, state_logger: Any = None) -> str:
        """
        Executes CrewAI Crew for Question Strategy & Phrasing.
        """
        task = create_question_generation_task(
            agent=self.strategist,
            role=role,
            difficulty=difficulty,
            topic=topic,
            previous_evaluation=previous_evaluation,
            resume_context=resume_context
        )

        crew = Crew(
            agents=[self.supervisor, self.strategist],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        if state_logger and hasattr(state_logger, "add_debug_entry"):
            state_logger.add_debug_entry(
                component="CrewAI",
                action="Executing Crew.kickoff() [Question Strategy Task]",
                details={"agents": ["Supervisor", "Question Strategist"], "topic": topic, "difficulty": difficulty}
            )

        try:
            result = crew.kickoff(inputs={
                "role": role,
                "difficulty": difficulty,
                "topic": topic
            })
            return str(result)
        except Exception as e:
            print(f"[CrewAI Question Strategy Warning] {e}")
            return f"Strategic question on {topic} for {role}."

    def run_answer_evaluation_crew(self, question: str, expected_answer: str, user_answer: str, state_logger: Any = None) -> str:
        """
        Executes CrewAI Crew for Technical Answer Evaluation.
        """
        task = create_answer_evaluation_task(
            agent=self.evaluator,
            question=question,
            expected_answer=expected_answer,
            user_answer=user_answer
        )

        crew = Crew(
            agents=[self.evaluator, self.supervisor],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        if state_logger and hasattr(state_logger, "add_debug_entry"):
            state_logger.add_debug_entry(
                component="CrewAI",
                action="Executing Crew.kickoff() [Answer Evaluation Task]",
                details={"agents": ["Answer Evaluator", "Supervisor"], "question": question[:60]}
            )

        try:
            result = crew.kickoff(inputs={
                "question": question,
                "expected_answer": expected_answer,
                "user_answer": user_answer
            })
            return str(result)
        except Exception as e:
            print(f"[CrewAI Evaluation Warning] {e}")
            return "Evaluated candidate answer."

    def run_final_report_crew(self, role: str, history_summary: str, state_logger: Any = None) -> str:
        """
        Executes CrewAI Crew for Final Report Generation.
        """
        task = create_final_report_task(
            agent=self.supervisor,
            role=role,
            history_summary=history_summary
        )

        crew = Crew(
            agents=[self.supervisor],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        if state_logger and hasattr(state_logger, "add_debug_entry"):
            state_logger.add_debug_entry(
                component="CrewAI",
                action="Executing Crew.kickoff() [Final Report Task]",
                details={"agents": ["Supervisor"], "role": role}
            )

        try:
            result = crew.kickoff(inputs={
                "role": role,
                "history": history_summary
            })
            return str(result)
        except Exception as e:
            print(f"[CrewAI Final Report Warning] {e}")
            return f"# Technical Interview Report for {role}\nEvaluation completed."
