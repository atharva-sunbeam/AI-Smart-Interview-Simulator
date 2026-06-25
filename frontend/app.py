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

if "question" not in st.session_state:
    st.session_state.question = None

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

        question = (
            controller.ask_question()
        )

        st.session_state.question = (
            question
        )


# --------------------------------------------------
# Question Display
# --------------------------------------------------

if st.session_state.question:

    st.subheader(
        "Interview Question"
    )

    st.info(
        st.session_state.question
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