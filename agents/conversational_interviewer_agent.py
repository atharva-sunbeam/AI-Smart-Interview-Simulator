"""
Conversational Interviewer Agent

Purpose:
Manage conversational interview flow.

Pipeline:

Question
    ↓
Candidate Answer
    ↓
Decision Engine
    ↓
Follow-up Question
OR
Next Topic
OR
End Interview
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from agents.question_generation_agent import (
    QuestionGenerationAgent,
)


class ConversationalInterviewerAgent:
    """
    Conversational Interview Brain.
    """

    FOLLOW_UP = "FOLLOW_UP"
    NEXT_TOPIC = "NEXT_TOPIC"
    END_INTERVIEW = "END_INTERVIEW"

    def __init__(self):

        self.question_agent = (
            QuestionGenerationAgent()
        )

        self.current_role = None
        self.current_topic = None

        self.current_difficulty = (
            "Medium"
        )

        self.followup_depth = 0
        self.max_followups = 2

        self.interview_history = []

    def start_interview(
        self,
        role
    ):
        """
        Initialize interview.
        """

        self.current_role = role
        self.followup_depth = 0
        self.interview_history = []

    def generate_initial_question(
        self,
        role,
        difficulty="Medium"
    ):
        """
        Generate initial interview question.
        """

        result = (
            self.question_agent.generate_question(
                role=role,
                difficulty=difficulty
            )
        )

        question = result["question"]

        self.current_topic = (
            self.extract_topic(
                question
            )
        )

        return {

            "question":
                question,

            "type":
                "INITIAL",

            "topic":
                self.current_topic,

            "difficulty":
                difficulty,
        }

    def generate_followup_question(
        self,
        previous_question,
        candidate_answer,
        interview_history=None
    ):
        """
        Generate rule-based follow-up question.
        """

        question_text = (
            previous_question.lower()
        )

        if "decorator" in question_text:

            followups = [

                "Can decorators accept parameters?",

                "Can you explain how decorators work internally?"
            ]

            index = min(
                self.followup_depth,
                len(followups) - 1
            )

            followup_question = (
                followups[index]
            )

            topic = "Decorators"

        elif "kafka" in question_text:

            followups = [

                "What are Kafka consumer groups?",

                "Explain Kafka rebalance protocol."
            ]

            index = min(
                self.followup_depth,
                len(followups) - 1
            )

            followup_question = (
                followups[index]
            )

            topic = "Kafka"

        else:

            followup_question = (
                "Can you explain this concept in more detail?"
            )

            topic = "General"

        self.followup_depth += 1

        return {

            "question":
                followup_question,

            "type":
                "FOLLOW_UP",

            "topic":
                topic,

            "difficulty":
                self.current_difficulty,
        }

    def decide_next_action(
        self,
        score,
        followup_depth=None
    ):
        """
        Decide next interview action.
        """

        if followup_depth is None:

            followup_depth = (
                self.followup_depth
            )

        if (
            followup_depth >=
            self.max_followups
        ):

            return self.NEXT_TOPIC

        if score < 40:

            return self.FOLLOW_UP

        elif score > 80:

            return self.NEXT_TOPIC

        return self.FOLLOW_UP

    def extract_topic(
        self,
        question
    ):
        """
        Extract topic from question.
        """

        question = question.lower()

        if "decorator" in question:
            return "Decorators"

        if "kafka" in question:
            return "Kafka"

        if "python" in question:
            return "Python"

        if "sql" in question:
            return "SQL"

        return "General"


if __name__ == "__main__":

    agent = (
        ConversationalInterviewerAgent()
    )

    agent.start_interview(
        "Python Developer"
    )

    question = (
        agent.generate_initial_question(
            "Python Developer"
        )
    )

    print(question)

    followup = (
        agent.generate_followup_question(
            question["question"],
            "Decorators modify functions."
        )
    )

    print(followup)