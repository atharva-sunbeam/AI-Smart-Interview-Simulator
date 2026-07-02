"""
Interview State Machine

Purpose:
Manage the complete interview lifecycle using
a finite-state machine (FSM).

Pipeline:

START
    ↓
INTRODUCTION
    ↓
QUESTION
    ↓
LISTENING
    ↓
THINKING
    ↓
FOLLOWUP
    ↓
NEXT_TOPIC
    ↓
SUMMARY
    ↓
END
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional


class InterviewState(Enum):
    """
    Interview lifecycle states.
    """

    START = "START"
    INTRODUCTION = "INTRODUCTION"
    QUESTION = "QUESTION"
    LISTENING = "LISTENING"
    THINKING = "THINKING"
    FOLLOWUP = "FOLLOWUP"
    NEXT_TOPIC = "NEXT_TOPIC"
    SUMMARY = "SUMMARY"
    END = "END"


@dataclass
class InterviewContext:
    """
    Stores the current interview context.
    """

    current_topic: str = ""

    current_question: str = ""

    previous_question: str = ""

    previous_answer: str = ""

    difficulty: str = "Easy"

    candidate_score: float = 0.0

    confidence_score: float = 0.0

    followup_count: int = 0

    interview_duration: int = 0

    conversation_history: List[dict] = field(
        default_factory=list
    )

    start_time: Optional[datetime] = None


class InterviewStateMachine:
    """
    Finite State Machine for interview flow.
    """

    def __init__(self):

        self.state = InterviewState.START

        self.context = InterviewContext()

    def start(self):
        """
        Begin interview.
        """

        self.context.start_time = (
            datetime.now()
        )

        self.state = (
            InterviewState.INTRODUCTION
        )

    def move_to_question(
        self,
        topic,
        question,
        difficulty="Easy",
    ):

        self.context.current_topic = topic

        self.context.current_question = question

        self.context.difficulty = difficulty

        self.state = (
            InterviewState.QUESTION
        )

    def start_listening(self):

        self.state = (
            InterviewState.LISTENING
        )

    def thinking(self):

        self.state = (
            InterviewState.THINKING
        )

    def followup(
        self,
        followup_question,
    ):

        self.context.previous_question = (
            self.context.current_question
        )

        self.context.current_question = (
            followup_question
        )

        self.context.followup_count += 1

        self.state = (
            InterviewState.FOLLOWUP
        )

    def next_topic(
        self,
        topic,
        question,
    ):

        self.context.previous_question = (
            self.context.current_question
        )

        self.context.current_topic = topic

        self.context.current_question = question

        self.state = (
            InterviewState.NEXT_TOPIC
        )

    def record_answer(
        self,
        answer,
        score,
    ):

        self.context.previous_answer = answer

        self.context.candidate_score = score

        self.context.conversation_history.append(
            {
                "topic":
                    self.context.current_topic,

                "question":
                    self.context.current_question,

                "answer":
                    answer,

                "score":
                    score,
            }
        )

    def summary(self):

        self.state = (
            InterviewState.SUMMARY
        )

    def end(self):

        if self.context.start_time:

            duration = (
                datetime.now()
                - self.context.start_time
            )

            self.context.interview_duration = (
                int(
                    duration.total_seconds()
                )
            )

        self.state = InterviewState.END

    def get_state(self):
        """
        Return current state.
        """

        return self.state

    def get_context(self):
        """
        Return interview context.
        """

        return self.context

    def reset(self):
        """
        Reset state machine.
        """

        self.state = InterviewState.START

        self.context = InterviewContext()


def main():

    machine = (
        InterviewStateMachine()
    )

    machine.start()

    print(machine.get_state())

    machine.move_to_question(
        topic="Python",
        question="Explain decorators.",
    )

    print(machine.get_state())

    machine.start_listening()

    print(machine.get_state())

    machine.thinking()

    print(machine.get_state())

    machine.record_answer(
        answer=(
            "Decorators extend functions."
        ),
        score=85,
    )

    machine.followup(
        "Can decorators accept arguments?"
    )

    print(machine.get_state())

    machine.summary()

    print(machine.get_state())

    machine.end()

    print(machine.get_state())

    print(machine.get_context())


if __name__ == "__main__":
    main()