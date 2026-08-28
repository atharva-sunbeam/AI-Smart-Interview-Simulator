import unittest
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.resume_agent import ResumeAgent
from rag_pipeline.rag import RAGPipeline
from agents.orchestrator import SuperAgent, LLMManager

class TestAIInterviewSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resume_agent = ResumeAgent()
        cls.rag = RAGPipeline()
        cls.rag.initialize_db(force_recreate=False)
        cls.super_agent = SuperAgent(cls.rag)

    def test_resume_parsing_expanded_roles(self):
        sample_resume = """
        Jane Doe - Senior AI Engineer & Cloud Architect
        Skills: Python, PyTorch, LangChain, RAG, Ollama, Docker, Kubernetes, AWS, Terraform, FastApi.
        Experienced in deploying LLM agent systems and scalable cloud infrastructure.
        """
        res = self.resume_agent.parse_resume(sample_resume)
        self.assertIn("LANGCHAIN", res["skills"])
        self.assertIn(res["recommended_role"], ["AI / LLM Engineer", "DevOps / Cloud Engineer", "Cloud Engineer (AWS / Azure / GCP)"])

    def test_rag_retrieval_and_self_learning(self):
        questions = self.rag.retrieve_questions(role="Python Developer", difficulty="Medium", k=2)
        self.assertTrue(len(questions) > 0)
        
        # Test self-learning insertion into ChromaDB
        test_history = [{
            "question": "What is the difference between shallow copy and deep copy in Python?",
            "answer": "Shallow copy creates a new object but inserts references to original objects. Deep copy creates independent copies recursively.",
            "topic": "Memory Management",
            "score": 9.0
        }]
        self.rag.add_session_to_knowledge_base(role="Python Developer", history_items=test_history)

    def test_super_agent_adaptive_workflow(self):
        # 1. Dynamic Question Synthesis
        questions = self.super_agent.get_questions(
            role="AI / LLM Engineer",
            difficulty="Medium",
            count=1,
            skills=["LANGCHAIN", "RAG"]
        )
        self.assertTrue(len(questions) > 0)
        q_item = questions[0]
        self.assertIn("question", q_item)
        self.assertIn("expected_answer", q_item)

        # 2. Main answer evaluation
        eval_res = self.super_agent.evaluate(
            question=q_item["question"],
            expected_answer=q_item["expected_answer"],
            user_answer="RAG retrieves relevant documents from vector store like ChromaDB and passes them to LLM prompt."
        )
        self.assertGreaterEqual(eval_res["score"], 1.0)
        self.assertLessEqual(eval_res["score"], 10.0)

        # 3. Adaptive difficulty stage progression test
        history_high = [{"score": 9.0}, {"score": 8.5}]
        new_diff = self.super_agent.get_adaptive_difficulty("Medium", history_high, adaptive_mode=True)
        self.assertEqual(new_diff, "Hard")

        history_low = [{"score": 3.0}, {"score": 4.0}]
        new_diff_low = self.super_agent.get_adaptive_difficulty("Medium", history_low, adaptive_mode=True)
        self.assertEqual(new_diff_low, "Easy")

        # 4. Report generation & self-learning save
        history = [
            {
                "question": q_item["question"],
                "topic": q_item["topic"],
                "score": eval_res["score"],
                "answer": "RAG retrieves relevant documents from vector store like ChromaDB.",
                "feedback": eval_res["feedback"]
            }
        ]
        report = self.super_agent.generate_report(role="AI / LLM Engineer", history=history)
        self.assertTrue("Technical Interview" in report or "Executive Summary" in report or "Report" in report)
        
        # Verify learning memory file creation
        memory_path = "datasets/processed/learning_memory.json"
        self.assertTrue(os.path.exists(memory_path))

if __name__ == "__main__":
    unittest.main()
