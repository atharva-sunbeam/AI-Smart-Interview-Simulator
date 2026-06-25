"""
Streamlit Frontend

Purpose:
Provide a web interface for the
AI Smart Interview Simulator.
"""

import sys
from pathlib import Path
import tempfile

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from agents.resume_parser import ResumeParser
from ml_models.role_prediction.train_role_classifier import (
    RoleClassifier,
)
from backend.interview_session import (
    InterviewSession,
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
# Session State Initialization
# --------------------------------------------------

if "session" not in st.session_state:
    st.session_state.session = InterviewSession()

if "predicted_role" not in st.session_state:
    st.session_state.predicted_role = None

if "question" not in st.session_state:
    st.session_state.question = None

if "evaluation" not in st.session_state:
    st.session_state.evaluation = None


# --------------------------------------------------
# Functions
# --------------------------------------------------

def upload_resume():
    """
    Upload resume PDF.
    """

    uploaded_file = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"]
    )

    return uploaded_file


def display_predicted_role(role):
    """
    Display predicted role.
    """

    st.success(
        f"Predicted Role: {role}"
    )


def show_question(question):
    """
    Display generated question.
    """

    st.subheader("Interview Question")

    st.info(question)


def accept_answer():
    """
    Accept candidate answer.
    """

    answer = st.text_area(
        "Enter Your Answer",
        height=200
    )

    return answer


def display_score(result):
    """
    Display evaluation score.
    """

    st.subheader("Evaluation")

    st.metric(
        "Score",
        result["score"]
    )

    st.write(
        f"Feedback: {result['feedback']}"
    )


def display_report(report):
    """
    Display final report.
    """

    st.subheader("Interview Report")

    st.json(report)


# --------------------------------------------------
# Main Workflow
# --------------------------------------------------

uploaded_resume = upload_resume()

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

    parser = ResumeParser()

    resume_text = (
        parser.extract_text_from_pdf(
            temp_resume_path
        )
    )

    cleaned_text = (
        parser.clean_resume_text(
            resume_text
        )
    )

    extracted_skills = (
        parser.extract_skills(
            cleaned_text
        )
    )

    st.subheader(
        "Extracted Skills"
    )

    st.write(extracted_skills)

    # ----------------------------------------
    # Role Prediction
    # ----------------------------------------

    try:

        classifier = RoleClassifier()

        classifier.load_model()

        predicted_role = (
            classifier.predict_role(
                cleaned_text
            )
        )

    except Exception:

        #
        # Fallback for demo purposes
        #
        predicted_role = (
            "Python Developer"
        )

    st.session_state.predicted_role = (
        predicted_role
    )

    display_predicted_role(
        predicted_role
    )

    # ----------------------------------------
    # Start Interview
    # ----------------------------------------

    if st.button(
        "Start Interview"
    ):

        session = (
            st.session_state.session
        )

        session.start_session(
            predicted_role
        )

        question = (
            session.ask_question()
        )

        st.session_state.question = (
            question
        )

# --------------------------------------------------
# Show Question
# --------------------------------------------------

if st.session_state.question:

    show_question(
        st.session_state.question
    )

    answer = accept_answer()

    if st.button(
        "Submit Answer"
    ):

        session = (
            st.session_state.session
        )

        session.submit_answer(
            answer
        )

        result = (
            session.evaluate_answer()
        )

        st.session_state.evaluation = (
            result
        )

# --------------------------------------------------
# Display Evaluation
# --------------------------------------------------

if st.session_state.evaluation:

    display_score(
        st.session_state.evaluation
    )

    report = (
        st.session_state.session
        .generate_report()
    )

    display_report(
        report
    )