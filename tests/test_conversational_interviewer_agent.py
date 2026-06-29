"""
Unit Tests:
Conversational Interviewer Agent
"""

from agents.conversational_interviewer_agent import (
    ConversationalInterviewerAgent
)


def test_agent_creation():

    agent = (
        ConversationalInterviewerAgent()
    )

    assert agent is not None
    assert agent.max_followups == 2


def test_initial_question_generation():

    agent = (
        ConversationalInterviewerAgent()
    )

    result = (
        agent.generate_initial_question(
            role="Python Developer",
            difficulty="Medium"
        )
    )

    assert "question" in result
    assert result["type"] == "INITIAL"


def test_followup_generation():

    agent = (
        ConversationalInterviewerAgent()
    )

    result = (
        agent.generate_followup_question(
            previous_question=
            "Explain decorators in Python.",

            candidate_answer=
            "Decorators modify functions.",

            interview_history=[]
        )
    )

    assert (
        result["type"]
        == "FOLLOW_UP"
    )

    assert (
        "question"
        in result
    )


def test_next_action_decision():

    agent = (
        ConversationalInterviewerAgent()
    )

    assert (

        agent.decide_next_action(
            score=20,
            followup_depth=0
        )

        ==

        "FOLLOW_UP"
    )

    assert (

        agent.decide_next_action(
            score=90,
            followup_depth=0
        )

        ==

        "NEXT_TOPIC"
    )