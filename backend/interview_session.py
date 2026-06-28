"""
Interview Session Orchestrator

Purpose:
Coordinate the complete interview workflow.

Pipeline:

Resume
    ↓
Role Prediction
    ↓
Question Generation
    ↓
Text-to-Speech
    ↓
Candidate Answer
    ↓
Speech-to-Text
    ↓
Answer Evaluation
    ↓
Interview Report
"""

import sys
import uuid
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from agents.question_generation_agent import (
    QuestionGenerationAgent,
)

from agents.answer_evaluation_agent import (
    AnswerEvaluationAgent,
)

from agents.speech_to_text_agent import (
    SpeechToTextAgent,
)

from agents.text_to_speech_agent import (
    TextToSpeechAgent,
)


class InterviewSession:
    """
    Orchestrates the complete interview process.
    """

    def __init__(self):

        self.question_agent = (
            QuestionGenerationAgent()
        )

        self.evaluator = (
            AnswerEvaluationAgent()
        )

        self.stt_agent = (
            SpeechToTextAgent()
        )

        self.tts_agent = (
            TextToSpeechAgent()
        )

        self.current_role = None
        self.current_question = None
        self.expected_answer = None
        self.current_answer = None
        self.current_audio_path = None

        self.session_history = []

    def start_session(
        self,
        predicted_role,
    ):
        """
        Start interview session.
        """

        self.current_role = predicted_role

        print("\nInterview Session Started")
        print(f"Role: {predicted_role}")

    def ask_question(self):
        """
        Generate interview question
        and corresponding audio.
        """

        if self.current_role is None:
            raise RuntimeError(
                "Interview session has not been started."
            )

        result = (
            self.question_agent.generate_question(
                self.current_role
            )
        )

        if not isinstance(result, dict):
            raise TypeError(
                "QuestionGenerationAgent must "
                "return a dictionary."
            )

        required_fields = (
            "question",
            "expected_answer",
        )

        for field in required_fields:

            if field not in result:
                raise KeyError(
                    f"Missing field: {field}"
                )

        self.current_question = (
            result["question"]
        )

        self.expected_answer = (
            result["expected_answer"]
        )

        #
        # Generate unique audio file
        #

        audio_filename = (
            f"{uuid.uuid4().hex}.mp3"
        )

        audio_path = (
            "audio/generated_questions/"
            + audio_filename
        )

        self.current_audio_path = (
            self.tts_agent.generate_audio(
                text=self.current_question,
                output_path=audio_path,
            )
        )

        return {
            "question":
                self.current_question,

            "expected_answer":
                self.expected_answer,

            "audio_path":
                self.current_audio_path,
        }

    def submit_answer(
        self,
        answer,
    ):
        """
        Submit text answer.
        """

        if self.current_question is None:
            raise RuntimeError(
                "No active interview question."
            )

        if not answer.strip():
            raise ValueError(
                "Candidate answer cannot be empty."
            )

        self.current_answer = answer

        print(
            "\nAnswer submitted successfully."
        )

    def submit_audio_answer(
        self,
        audio_path,
    ):
        """
        Speech
            ↓
        Transcript
            ↓
        Submit Answer
        """

        result = (
            self.stt_agent.transcribe_audio(
                audio_path
            )
        )

        transcript = (
            result["transcript"]
        )

        self.submit_answer(
            transcript
        )

        return result

    def evaluate_answer(self):
        """
        Evaluate candidate answer.
        """

        if self.current_question is None:
            raise RuntimeError(
                "No interview question available."
            )

        if self.expected_answer is None:
            raise RuntimeError(
                "Expected answer unavailable."
            )

        if self.current_answer is None:
            raise RuntimeError(
                "Candidate answer not submitted."
            )

        result = (
            self.evaluator.evaluate_answer(
                expected_answer=self.expected_answer,
                candidate_answer=self.current_answer,
            )
        )

        interview_record = {

            "role":
                self.current_role,

            "question":
                self.current_question,

            "audio_path":
                self.current_audio_path,

            "expected_answer":
                self.expected_answer,

            "candidate_answer":
                self.current_answer,

            "score":
                result["score"],

            "feedback":
                result["feedback"],
        }

        self.session_history.append(
            interview_record
        )

        #
        # Reset state for next question
        #

        self.current_question = None
        self.expected_answer = None
        self.current_answer = None
        self.current_audio_path = None

        return result

    def generate_report(self):
        """
        Generate interview report.
        """

        total_questions = len(
            self.session_history
        )

        if total_questions == 0:

            return {
                "role":
                    self.current_role,

                "total_questions":
                    0,

                "average_score":
                    0,

                "details":
                    [],
            }

        total_score = sum(
            record["score"]
            for record in self.session_history
        )

        average_score = round(
            total_score / total_questions,
            2,
        )

        return {

            "role":
                self.current_role,

            "total_questions":
                total_questions,

            "average_score":
                average_score,

            "details":
                self.session_history,
        }


if __name__ == "__main__":

    session = InterviewSession()

    session.start_session(
        "Data Engineer"
    )

    question = (
        session.ask_question()
    )

    print("\nQuestion")
    print(question["question"])

    print("\nAudio File")
    print(question["audio_path"])

    session.submit_answer(
        "Kafka consists of producers, brokers, topics, partitions and consumers."
    )

    result = (
        session.evaluate_answer()
    )

    print("\nEvaluation")
    print(result)

    report = (
        session.generate_report()
    )

    print("\nFinal Report")
    print(report)