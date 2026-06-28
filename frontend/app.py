"""
Streamlit Frontend

Purpose:
Provide UI for the AI Smart Interview Simulator.

Architecture:

Streamlit UI
      ↓
SystemController
      ↓
Complete Backend
"""

import os
import sys
import tempfile
import uuid
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from backend.system_controller import (
    SystemController,
)

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Smart Interview Simulator",
    page_icon="🤖",
    layout="wide",
)

st.title(
    "🤖 AI Smart Interview Simulator"
)

st.markdown("---")

# --------------------------------------------------
# Session State
# --------------------------------------------------

if "controller" not in st.session_state:
    st.session_state.controller = (
        SystemController()
    )

if "predicted_role" not in st.session_state:
    st.session_state.predicted_role = None

if "question_data" not in st.session_state:
    st.session_state.question_data = None

if "evaluation" not in st.session_state:
    st.session_state.evaluation = None

if "voice_evaluation" not in st.session_state:
    st.session_state.voice_evaluation = None

if "transcript" not in st.session_state:
    st.session_state.transcript = ""

if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

if "resume_processed" not in st.session_state:
    st.session_state.resume_processed = False

# --------------------------------------------------
# Resume Upload
# --------------------------------------------------

uploaded_resume = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

# --------------------------------------------------
# Resume Processing
# --------------------------------------------------

if (
    uploaded_resume
    and
    not st.session_state.resume_processed
):

    # Reset previous session

    st.session_state.question_data = None
    st.session_state.evaluation = None
    st.session_state.voice_evaluation = None
    st.session_state.transcript = ""
    st.session_state.interview_started = False

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        temp_file.write(
            uploaded_resume.read()
        )

        temp_resume_path = (
            temp_file.name
        )

    controller = (
        st.session_state.controller
    )

    result = (
        controller.run_complete_pipeline(
            temp_resume_path
        )
    )

    os.remove(
        temp_resume_path
    )

    st.session_state.predicted_role = (
        result["role"]
    )

    st.session_state.resume_processed = True

    st.success(
        "Resume uploaded successfully."
    )

    st.subheader(
        "Extracted Skills"
    )

    st.write(
        result["skills"]
    )

    st.success(
        f"Predicted Role: {result['role']}"
    )

# --------------------------------------------------
# Start Interview
# --------------------------------------------------

if (
    st.session_state.predicted_role
    and
    not st.session_state.interview_started
):

    if st.button(
        "Start Interview"
    ):

        controller = (
            st.session_state.controller
        )

        controller.start_interview(
            st.session_state.predicted_role
        )

        st.session_state.question_data = (
            controller.ask_question()
        )

        st.session_state.interview_started = (
            True
        )

        st.rerun()

# --------------------------------------------------
# Interview Section
# --------------------------------------------------

if st.session_state.question_data:

    question_data = (
        st.session_state.question_data
    )

    current_question = (
        question_data.get(
            "question_number",
            1
        )
    )

    max_questions = (
        question_data.get(
            "max_questions",
            5
        )
    )

    difficulty = (
        question_data.get(
            "difficulty",
            "Medium"
        )
    )

    st.progress(
        current_question / max_questions
    )

    st.info(
        f"Question {current_question} "
        f"of {max_questions}"
    )

    st.caption(
        f"Difficulty: {difficulty}"
    )

    st.caption(
        "⏱ Recommended time: 2 minutes"
    )

    st.subheader(
        "Interview Question"
    )

    st.write(
        question_data["question"]
    )

    audio_path = (
        question_data.get(
            "audio_path"
        )
    )

    if audio_path:

        st.subheader(
            "🔊 Listen Question"
        )

        st.audio(
            audio_path,
            format="audio/mp3"
        )

    # ------------------------------------------
    # Text Answer
    # ------------------------------------------

    answer = st.text_area(
        "Enter Your Answer",
        height=200
    )

    if st.button(
        "Submit Text Answer"
    ):

        if not answer.strip():

            st.warning(
                "Please enter an answer."
            )

        else:

            controller = (
                st.session_state.controller
            )

            controller.submit_answer(
                answer
            )

            st.session_state.evaluation = (
                controller.evaluate_answer()
            )

            st.session_state.question_data = None

            st.rerun()

    # ------------------------------------------
    # Voice Answer
    # ------------------------------------------

    st.markdown("---")

    st.subheader(
        "🎤 Voice Answer"
    )

    audio_file = st.file_uploader(
        "Upload Answer Audio",
        type=[
            "wav",
            "mp3",
            "m4a",
            "ogg"
        ]
    )

    if audio_file:

        audio_directory = (
            PROJECT_ROOT
            / "audio"
            / "candidate_answers"
        )

        audio_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        audio_path = (
            audio_directory /
            f"{uuid.uuid4().hex}_"
            f"{audio_file.name}"
        )

        with open(
            audio_path,
            "wb"
        ) as file:

            file.write(
                audio_file.getbuffer()
            )

        try:

            result = (
                st.session_state.controller
                .interview_session
                .submit_audio_answer(
                    str(audio_path)
                )
            )

            st.session_state.transcript = (
                result["transcript"]
            )

            st.success(
                "Audio transcribed successfully."
            )

            if os.path.exists(
                audio_path
            ):
                os.remove(
                    audio_path
                )

        except Exception as error:

            st.error(error)

    st.subheader(
        "📝 Transcript"
    )

    edited_transcript = st.text_area(
        "Recognized Speech",
        value=st.session_state.transcript,
        height=150
    )

    st.session_state.transcript = (
        edited_transcript
    )

    if st.button(
        "Evaluate Voice Answer"
    ):

        if not st.session_state.transcript.strip():

            st.warning(
                "Please upload and transcribe audio first."
            )

        else:

            try:

                controller = (
                    st.session_state.controller
                )

                controller.submit_answer(
                    st.session_state.transcript
                )

                st.session_state.voice_evaluation = (
                    controller.evaluate_answer()
                )

                st.session_state.question_data = None
                st.session_state.transcript = ""

                st.rerun()

            except Exception as error:

                st.error(error)

# --------------------------------------------------
# Evaluation Section
# --------------------------------------------------

latest_evaluation = (
    st.session_state.evaluation
    or
    st.session_state.voice_evaluation
)

if latest_evaluation:

    st.markdown("---")

    st.subheader(
        "Evaluation"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Score",
            latest_evaluation["score"]
        )

    with col2:

        st.metric(
            "Next Difficulty",
            st.session_state.controller
            .interview_session
            .current_difficulty
        )

    st.success(
        latest_evaluation["feedback"]
    )

    session = (
        st.session_state.controller
        .interview_session
    )

    # --------------------------------------
    # Next Question
    # --------------------------------------

    if not session.interview_completed():

        if st.button(
            "Next Question"
        ):

            st.session_state.evaluation = None
            st.session_state.voice_evaluation = None

            st.session_state.question_data = (
                st.session_state.controller
                .ask_question()
            )

            st.rerun()

    else:

        st.success(
            "🎉 Interview Completed Successfully!"
        )

        report = (
            st.session_state.controller
            .generate_report()
        )

        st.subheader(
            "Final Interview Report"
        )

        st.json(
            report
        )