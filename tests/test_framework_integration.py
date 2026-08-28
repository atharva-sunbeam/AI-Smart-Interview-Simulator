import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.interview_state import InterviewState
from core.llm_factory import LLMFactory
from core.interview_controller import InterviewController
from langchain_layer.schemas import AnswerEvaluation, InterviewDecision
from langchain_layer.tools import (
    retrieve_knowledge,
    retrieve_role_questions,
    retrieve_resume_context,
    evaluate_answer_tool
)
from crew_layer.agents import create_interview_crew_agents
from crew_layer.tasks import create_question_generation_task, create_answer_evaluation_task
from crew_layer.interview_crew import InterviewCrewOrchestrator


class TestFrameworkIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.llm_factory = LLMFactory()
        cls.controller = InterviewController()

    def test_01_centralized_interview_state(self):
        state = InterviewState(
            target_role="Data Engineer",
            difficulty="Medium",
            candidate_name="Alice"
        )
        self.assertEqual(state.target_role, "Data Engineer")
        self.assertEqual(state.difficulty, "Medium")
        
        state.add_debug_entry("TestComponent", "TestAction", {"key": "val"})
        self.assertEqual(len(state.debug_logs), 1)
        self.assertEqual(state.debug_logs[0]["component"], "TestComponent")

        state.add_transcript_turn("interviewer", "What is Spark?")
        self.assertEqual(len(state.transcript), 1)
        self.assertEqual(state.transcript[0]["message"], "What is Spark?")

    def test_02_langchain_tools_execution(self):
        # 1. RAG retrieval tool
        rag_res = retrieve_knowledge.invoke({"query": "spark etl", "role": "Data Engineer", "difficulty": "Medium"})
        self.assertIsInstance(rag_res, str)

        # 2. Knowledge bank question retrieval tool
        role_qs = retrieve_role_questions.invoke({"role": "Data Engineer", "difficulty": "Easy", "topic": "Python"})
        self.assertIsInstance(role_qs, str)

        # 3. Resume context retrieval tool
        resume_data = {"skills": ["SPARK", "PYTHON"], "projects": [{"name": "Pipeline", "tools": ["Kafka"], "description": "Stream processing"}]}
        resume_res = retrieve_resume_context.invoke({"resume_json": str(resume_data).replace("'", '"')})
        self.assertIn("SPARK", resume_res)

        # 4. Structured Answer Evaluation tool
        eval_res = evaluate_answer_tool.invoke({
            "question": "What is PySpark?",
            "expected_answer": "PySpark is the Python API for Apache Spark allowing distributed data processing.",
            "candidate_answer": "PySpark provides Python bindings for Apache Spark for large scale data processing."
        })
        self.assertIn("technical_score", eval_res)

    def test_03_langchain_agent_service(self):
        service = self.controller.langchain_service
        self.assertIsNotNone(service)
        
        # Test structured answer evaluation
        struct_eval = service.evaluate_candidate_answer(
            question="What is garbage collection?",
            expected_answer="Automatic memory recovery by identifying unused objects.",
            user_answer="It automatically reclaims memory by deleting unreferenced objects."
        )
        self.assertIsInstance(struct_eval, AnswerEvaluation)
        self.assertGreaterEqual(struct_eval.technical_score, 1.0)
        self.assertLessEqual(struct_eval.technical_score, 10.0)

        # Test structured decision generation
        decision = service.generate_next_interview_decision(
            role="Python Developer",
            difficulty="Easy",
            topic="Memory Management",
            past_questions=[]
        )
        self.assertIsInstance(decision, InterviewDecision)
        self.assertTrue(len(decision.next_question) > 0)

    def test_04_crewai_agent_and_task_construction(self):
        agents = create_interview_crew_agents(self.llm_factory)
        self.assertIn("supervisor", agents)
        self.assertIn("strategist", agents)
        self.assertIn("interviewer", agents)
        self.assertIn("evaluator", agents)

        task_q = create_question_generation_task(
            agent=agents["strategist"],
            role="Linux System Administrator",
            difficulty="Easy",
            topic="Linux Commands"
        )
        self.assertIsNotNone(task_q)
        self.assertEqual(task_q.agent.role, "Question Strategy Agent")

        task_eval = create_answer_evaluation_task(
            agent=agents["evaluator"],
            question="What is bash?",
            expected_answer="Shell scripting language",
            user_answer="Command line shell"
        )
        self.assertEqual(task_eval.agent.role, "Technical Answer Evaluator Agent")

    def test_05_crewai_crew_kickoff_execution(self):
        orchestrator = self.controller.crew_orchestrator
        self.assertIsNotNone(orchestrator)
        
        # Test Question Strategy Crew kickoff
        crew_q_res = orchestrator.run_question_strategy_crew(
            role="Network Administrator",
            difficulty="Easy",
            topic="DNS & Subnetting",
            state_logger=self.controller.state
        )
        self.assertIsInstance(crew_q_res, str)
        self.assertTrue(len(crew_q_res) > 0)

        # Test Answer Evaluation Crew kickoff
        crew_eval_res = orchestrator.run_answer_evaluation_crew(
            question="What is DNS?",
            expected_answer="Domain Name System translates domain names to IP addresses.",
            user_answer="DNS resolves domain names into IP addresses.",
            state_logger=self.controller.state
        )
        self.assertIsInstance(crew_eval_res, str)

    def test_06_controller_end_to_end_adaptive_flow(self):
        self.controller.initialize_session(
            role="AI / LLM Engineer",
            difficulty="Medium",
            count=3,
            resume_context={
                "skills": ["LANGCHAIN", "RAG", "PYTHON"],
                "projects": [{"name": "Smart Interview Simulator", "tools": ["LANGCHAIN", "CREWAI"], "description": "AI interview platform"}]
            }
        )
        
        # 1. Generate Question 1
        q1 = self.controller.generate_next_question()
        self.assertIn("question", q1)
        self.assertTrue(len(self.controller.state.asked_questions) == 1)

        # 2. Evaluate candidate response
        eval1 = self.controller.evaluate_candidate_answer("LangChain provides component abstractions for building LLM applications.")
        self.assertIn("score", eval1)

        # 3. Generate adaptive follow-up
        fu = self.controller.generate_followup_question("I used Chroma DB for vector search.")
        self.assertTrue(len(fu) > 0)

        # 4. Generate final report
        report = self.controller.generate_final_report()
        self.assertIn("Report", report)
        
        # 5. Verify live debug log entries recorded
        debug_logs = self.controller.state.debug_logs
        components_logged = {log["component"] for log in debug_logs}
        self.assertIn("CrewAI", components_logged)
        self.assertIn("LangChain", components_logged)
        self.assertIn("Controller", components_logged)


if __name__ == "__main__":
    unittest.main()
