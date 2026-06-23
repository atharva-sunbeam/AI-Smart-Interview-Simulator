from agents.answer_evaluation_agent import (
AnswerEvaluationAgent,
)

def test_evaluate_answer():

    
    agent = AnswerEvaluationAgent()

    result = agent.evaluate_answer(
        expected_answer=(
            "Python is a programming language."
        ),
        candidate_answer=(
            "Python is a programming language."
        ),
    )

    assert "score" in result
    assert "feedback" in result
    

def test_score_range():

    agent = AnswerEvaluationAgent()

    result = agent.evaluate_answer(
        expected_answer="Python",
        candidate_answer="Python",
    )

    assert 0 <= result["score"] <= 100
    
