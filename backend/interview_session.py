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
Adaptive Difficulty
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

        # Interview settings

        self.max_questions = 5
        self.questions_asked = 0

        self.current_difficulty = (
            "Medium"
        )

        self.question_difficulty = (
            "Medium"
        )

        self.session_history = []

    def start_session(
        self,
        predicted_role,
    ):

        self.current_role = predicted_role

        self.questions_asked = 0

        self.current_difficulty = (
            "Medium"
        )

        self.session_history = []

        print("\nInterview Session Started")
        print(f"Role: {predicted_role}")

    def ask_question(self):

        if self.current_role is None:

            raise RuntimeError(
                "Interview session has not been started."
            )

        self.question_difficulty = (
            self.current_difficulty
        )

        result = (
            self.question_agent.generate_question(
                role=self.current_role,
                difficulty=self.current_difficulty
            )
        )

        self.current_question = (
            result["question"]
        )

        self.expected_answer = (
            result["expected_answer"]
        )

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
                output_path=audio_path
            )
        )

        return {

            "question":
                self.current_question,

            "expected_answer":
                self.expected_answer,

            "audio_path":
                self.current_audio_path,

            "difficulty":
                self.question_difficulty,

            "question_number":
                self.questions_asked + 1,

            "max_questions":
                self.max_questions
        }

    def submit_answer(
        self,
        answer,
    ):

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

        return (
            self.stt_agent.transcribe_audio(
                audio_path
            )
        )

    def update_difficulty(
        self,
        score
    ):

        if score >= 80:

            self.current_difficulty = (
                "Hard"
            )

        elif score < 50:

            self.current_difficulty = (
                "Easy"
            )

        else:

            self.current_difficulty = (
                "Medium"
            )

    def interview_completed(self):

        return (
            self.questions_asked
            >=
            self.max_questions
        )

    def evaluate_answer(self):

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
                expected_answer=
                    self.expected_answer,

                candidate_answer=
                    self.current_answer
            )
        )

        score = result["score"]

        self.questions_asked += 1

        interview_record = {

            "role":
                self.current_role,

            "question":
                self.current_question,

            "difficulty":
                self.question_difficulty,

            "audio_path":
                self.current_audio_path,

            "expected_answer":
                self.expected_answer,

            "candidate_answer":
                self.current_answer,

            "score":
                score,

            "similarity":
                result.get(
                    "similarity",
                    0
                ),

            "feedback":
                result["feedback"]
        }

        self.session_history.append(
            interview_record
        )

        self.update_difficulty(
            score
        )

        # Cleanup audio

        if (
            self.current_audio_path
            and
            Path(
                self.current_audio_path
            ).exists()
        ):

            Path(
                self.current_audio_path
            ).unlink()

        self.current_question = None
        self.expected_answer = None
        self.current_answer = None
        self.current_audio_path = None

        return result

    def generate_report(self):

        total_questions = len(
            self.session_history
        )

        if total_questions == 0:

            return {
                "role": self.current_role,
                "total_questions": 0,
                "average_score": 0,
                "details": []
            }

        total_score = sum(
            item["score"]
            for item
            in self.session_history
        )

        average_score = round(
            total_score / total_questions,
            2
        )

        strengths = []
        weaknesses = []

        for item in self.session_history:

            if item["score"] >= 80:

                strengths.append(
                    item["question"]
                )

            elif item["score"] < 50:

                weaknesses.append(
                    item["question"]
                )

        if average_score >= 80:

            overall_result = (
                "Excellent"
            )

        elif average_score >= 60:

            overall_result = (
                "Good"
            )

        else:

            overall_result = (
                "Needs Improvement"
            )

        return {

            "role":
                self.current_role,

            "total_questions":
                total_questions,

            "average_score":
                average_score,

            "overall_result":
                overall_result,

            "strengths":
                strengths,

            "weaknesses":
                weaknesses,

            "details":
                self.session_history
        }


if __name__ == "__main__":

    session = InterviewSession()

    session.start_session(
        "Data Engineer"
    )

    while not session.interview_completed():

        question = (
            session.ask_question()
        )

        print(
            "\nQuestion:"
        )

        print(
            question["question"]
        )

        session.submit_answer(
            "Kafka consists of producers, brokers, topics and consumers."
        )

        result = (
            session.evaluate_answer()
        )

        print(
            result
        )

    print(
        "\nFinal Report"
    )

    print(
        session.generate_report()
    )

