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

st.title("🤖 AI Smart Interview Simulator")
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

if uploaded_resume:

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        temp_file.write(
            uploaded_resume.read()
        )

        temp_resume_path = temp_file.name

    st.success(
        "Resume uploaded successfully."
    )

    controller = (
        st.session_state.controller
    )

    result = controller.run_complete_pipeline(
        temp_resume_path
    )

    os.remove(
        temp_resume_path
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

    st.session_state.predicted_role = (
        result["role"]
    )

    if st.button(
        "Start Interview"
    ):

        controller.start_interview(
            result["role"]
        )

        question_data = (
            controller.ask_question()
        )

        st.session_state.question_data = (
            question_data
        )


# --------------------------------------------------
# Question Display
# --------------------------------------------------

if st.session_state.question_data:

    st.markdown("### Interview Question")

    st.write(
        st.session_state.question_data[
            "question"
        ]
    )

    audio_path = (
    st.session_state.question_data.get(
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

    if st.button(
        "🎧 Replay Question"
    ):

        st.audio(
            audio_path,
            format="audio/mp3"
        )

    answer = st.text_area(
        "Enter Your Answer",
        height=200
    )

    if st.button(
        "Submit Answer"
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

            evaluation = (
                controller.evaluate_answer()
            )

            st.session_state.evaluation = (
                evaluation
            )
            st.session_state.question_data = None

# ===================================
# Voice Answer Section
# ===================================

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

transcript = ""

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
        audio_directory
        / audio_file.name
    )

    with open(
        audio_path,
        "wb"
    ) as file:

        file.write(
            audio_file.getbuffer()
        )

    try:

        st.info(
            "Transcribing audio..."
        )

        result = (
            st.session_state.controller
            .interview_session
            .submit_audio_answer(
                str(audio_path)
            )
        )

        transcript = (
            result["transcript"]
        )

        st.subheader(
            "📝 Transcript"
        )

        st.text_area(
            "Recognized Speech",
            transcript,
            height=150
        )

    except Exception as error:

        st.error(error)
        

# --------------------------------------------------
# Evaluation
# --------------------------------------------------

if st.session_state.evaluation:

    st.subheader(
        "Evaluation"
    )

    st.metric(
        "Score",
        st.session_state.evaluation["score"]
    )

    st.write(
        f"Feedback: "
        f"{st.session_state.evaluation['feedback']}"
    )

    report = (
        st.session_state.controller
        .generate_report()
    )

    st.subheader(
        "Interview Report"
    )

    st.json(
        report
    )