import sys
import os

# Add workspace directory to python path
sys.path.insert(0, os.path.abspath("."))

from agents.role_catalog import get_all_roles, get_related_roles
from agents.knowledge_manager import KnowledgeManager
from agents.orchestrator import SuperAgent, LLMManager
from rag_pipeline.rag import RAGPipeline

def test_related_roles_tech_stack_clusters():
    print("\n--- Testing Tech Stack Related Roles Clusters ---")
    bda_sister_roles = get_related_roles("Data Analyst")
    print(f"Data Analyst Sister Roles: {bda_sister_roles[:4]}")
    assert len(bda_sister_roles) > 0, "Data Analyst should have sister roles in Data/AI cluster"
    assert "Data Engineer" in bda_sister_roles or "Machine Learning Engineer" in bda_sister_roles

    itiss_sister_roles = get_related_roles("Linux System Administrator")
    print(f"Linux System Administrator Sister Roles: {itiss_sister_roles[:4]}")
    assert len(itiss_sister_roles) > 0, "Linux System Admin should have sister roles in Infra/Cloud cluster"
    assert "Network Administrator" in itiss_sister_roles or "Cyber Security Analyst" in itiss_sister_roles

def test_cross_course_knowledge_retrieval():
    print("\n--- Testing Shared Tech Stack Question Retrieval ---")
    km = KnowledgeManager()

    # Query Data Analyst which pulls from Data/AI cluster
    data_qs = km.get_questions_for_role("Data Analyst", "Easy", topic="Python")
    print(f"Loaded {len(data_qs)} Python questions for Data Analyst including sister pools.")
    assert len(data_qs) > 0, "Should retrieve Python questions from Data/AI cluster"

    # Query Linux System Admin which pulls from Infra/Security cluster
    linux_qs = km.get_questions_for_role("Linux System Administrator", "Easy", topic="Linux")
    print(f"Loaded {len(linux_qs)} Linux questions for Linux Admin including sister pools.")
    assert len(linux_qs) > 0, "Should retrieve Linux questions from Infra/Security cluster"

if __name__ == "__main__":
    test_related_roles_tech_stack_clusters()
    test_cross_course_knowledge_retrieval()
    print("\n[SUCCESS] Knowledge Base Tech Stack Tests Passed!")
