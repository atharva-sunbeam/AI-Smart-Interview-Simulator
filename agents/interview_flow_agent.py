"""
Interview Flow Agent

Purpose:
Control the logical flow of the interview.

Responsibilities:

- Decide whether to ask a follow-up
- Decide whether to move to the next topic
- Decide interview difficulty
- Decide when to end interview

The Interview Flow Agent DOES NOT own the
interview state. It only reads the
InterviewStateMachine and recommends
the next action.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from backend.interview_state_machine import (
    InterviewState,
    InterviewStateMachine,
)


class InterviewFlowAgent:
    """
    Controls interview flow decisions.
    """

    def __init__(
        self,
        state_machine: InterviewStateMachine,
    ):

        self.state_machine = state_machine

    def should_ask_followup(self):
        """
        Decide whether a follow-up question
        should be asked.
        """

        context = (
            self.state_machine.get_context()
        )

        # Weak answer
        if context.candidate_score < 60:

            return True

        # Too many follow-ups already
        if context.followup_count >= 2:

            return False

        return False

    def should_change_topic(self):
        """
        Decide whether to move
        to the next topic.
        """

        context = (
            self.state_machine.get_context()
        )

        if context.candidate_score >= 60:

            return True

        return False

    def next_difficulty(self):
        """
        Recommend interview difficulty.
        """

        score = (
            self.state_machine
            .get_context()
            .candidate_score
        )

        if score >= 85:
            return "Hard"

        if score >= 70:
            return "Medium"

        return "Easy"

    def should_end_interview(self):
        """
        Decide whether interview
        should end.
        """

        context = (
            self.state_machine.get_context()
        )

        # Example rule:
        # End after 5 questions.

        if len(
            context.conversation_history
        ) >= 5:

            return True

        return False

    def next_action(self):
        """
        Decide the next state transition.

        Returns one of:

        FOLLOWUP
        NEXT_TOPIC
        SUMMARY
        """

        current_state = (
            self.state_machine.get_state()
        )

        if current_state != InterviewState.THINKING:

            return current_state

        if self.should_end_interview():

            return InterviewState.SUMMARY

        if self.should_ask_followup():

            return InterviewState.FOLLOWUP

        if self.should_change_topic():

            return InterviewState.NEXT_TOPIC

        return InterviewState.FOLLOWUP

    def interview_status(self):
        """
        Return complete interview status.
        """

        context = (
            self.state_machine.get_context()
        )

        return {

            "state":
                self.state_machine
                .get_state()
                .value,

            "topic":
                context.current_topic,

            "difficulty":
                context.difficulty,

            "score":
                context.candidate_score,

            "followups":
                context.followup_count,

            "questions":
                len(
                    context.conversation_history
                ),

            "duration":
                context.interview_duration,

            "confidence":
                context.confidence_score,
        }


def main():

    machine = (
        InterviewStateMachine()
    )

    flow = (
        InterviewFlowAgent(
            machine
        )
    )

    machine.start()

    machine.move_to_question(
        topic="Python",
        question="Explain decorators.",
    )

    machine.start_listening()

    machine.thinking()

    machine.record_answer(
        answer="Decorators extend functions.",
        score=82,
    )

    print("\nInterview Status\n")

    print(
        flow.interview_status()
    )

    print("\nNext Action\n")

    print(
        flow.next_action()
    )

    print("\nRecommended Difficulty\n")

    print(
        flow.next_difficulty()
    )


if __name__ == "__main__":
    main()