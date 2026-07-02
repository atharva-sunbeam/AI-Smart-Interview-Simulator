"""
Unit Tests for Interview State Machine

Purpose:
Validate the finite-state machine used by
the interview engine.

Tests:
- Initial state
- State transitions
- Follow-up state
- End state
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from backend.interview_state_machine import (
    InterviewState,
    InterviewStateMachine,
)


def test_initial_state():
    """
    Verify initial state is START.
    """

    machine = InterviewStateMachine()

    assert (
        machine.get_state()
        == InterviewState.START
    )


def test_start_transition():
    """
    Verify START → INTRODUCTION.
    """

    machine = InterviewStateMachine()

    machine.start()

    assert (
        machine.get_state()
        == InterviewState.INTRODUCTION
    )


def test_question_transition():
    """
    Verify QUESTION state.
    """

    machine = InterviewStateMachine()

    machine.start()

    machine.move_to_question(
        topic="Python",
        question="Explain decorators.",
    )

    assert (
        machine.get_state()
        == InterviewState.QUESTION
    )

    context = machine.get_context()

    assert (
        context.current_topic
        == "Python"
    )

    assert (
        context.current_question
        == "Explain decorators."
    )


def test_listening_transition():
    """
    Verify QUESTION → LISTENING.
    """

    machine = InterviewStateMachine()

    machine.start()

    machine.move_to_question(
        "Python",
        "Explain decorators."
    )

    machine.start_listening()

    assert (
        machine.get_state()
        == InterviewState.LISTENING
    )


def test_thinking_transition():
    """
    Verify LISTENING → THINKING.
    """

    machine = InterviewStateMachine()

    machine.start()

    machine.move_to_question(
        "Python",
        "Explain decorators."
    )

    machine.start_listening()

    machine.thinking()

    assert (
        machine.get_state()
        == InterviewState.THINKING
    )


def test_record_answer():
    """
    Verify answer recording.
    """

    machine = InterviewStateMachine()

    machine.start()

    machine.move_to_question(
        "Python",
        "Explain decorators."
    )

    machine.record_answer(
        answer="Decorators modify functions.",
        score=88,
    )

    context = machine.get_context()

    assert (
        context.previous_answer
        == "Decorators modify functions."
    )

    assert (
        context.candidate_score
        == 88
    )

    assert (
        len(
            context.conversation_history
        )
        == 1
    )


def test_followup_state():
    """
    Verify FOLLOWUP transition.
    """

    machine = InterviewStateMachine()

    machine.start()

    machine.move_to_question(
        "Python",
        "Explain decorators."
    )

    machine.followup(
        "Can decorators accept arguments?"
    )

    assert (
        machine.get_state()
        == InterviewState.FOLLOWUP
    )

    context = machine.get_context()

    assert (
        context.followup_count
        == 1
    )

    assert (
        context.previous_question
        == "Explain decorators."
    )

    assert (
        context.current_question
        == "Can decorators accept arguments?"
    )


def test_next_topic():
    """
    Verify NEXT_TOPIC transition.
    """

    machine = InterviewStateMachine()

    machine.start()

    machine.move_to_question(
        "Python",
        "Explain decorators."
    )

    machine.next_topic(
        topic="OOP",
        question="Explain inheritance."
    )

    assert (
        machine.get_state()
        == InterviewState.NEXT_TOPIC
    )

    context = machine.get_context()

    assert (
        context.current_topic
        == "OOP"
    )

    assert (
        context.current_question
        == "Explain inheritance."
    )


def test_summary_state():
    """
    Verify SUMMARY transition.
    """

    machine = InterviewStateMachine()

    machine.summary()

    assert (
        machine.get_state()
        == InterviewState.SUMMARY
    )


def test_end_state():
    """
    Verify END transition.
    """

    machine = InterviewStateMachine()

    machine.start()

    machine.end()

    assert (
        machine.get_state()
        == InterviewState.END
    )


def test_reset():
    """
    Verify reset functionality.
    """

    machine = InterviewStateMachine()

    machine.start()

    machine.move_to_question(
        "Python",
        "Explain decorators."
    )

    machine.reset()

    assert (
        machine.get_state()
        == InterviewState.START
    )

    context = machine.get_context()

    assert (
        context.current_topic
        == ""
    )

    assert (
        len(
            context.conversation_history
        )
        == 0
    )