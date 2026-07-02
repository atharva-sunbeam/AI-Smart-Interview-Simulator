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
from agents.realtime_audio_agent import (
    RealtimeAudioAgent,
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

if "realtime_audio" not in st.session_state:

    st.session_state.realtime_audio = (
        RealtimeAudioAgent()
    )

if "live_listening" not in st.session_state:

    st.session_state.live_listening = False

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
            "🤖 AI Interviewer"
        )

        st.info(
            "🔊 AI is asking the interview question..."
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
    # Live Voice Interview
    # ------------------------------------------

    st.markdown("---")

    st.subheader(
        "🎤 Candidate Response"
    )

    st.caption(
        "Answer naturally as if speaking to a real interviewer."
    )

    audio_agent = (
        st.session_state.realtime_audio
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🎤 Start Speaking"
        ):

            audio_agent.clear_transcript()

            audio_agent.start_stream()

            st.session_state.live_listening = True

    with col2:

        if st.button(
            "⏹ Stop Speaking"
        ):

            audio_agent.stop_stream()

            st.session_state.live_listening = False

    # ------------------------------------------

    if st.session_state.live_listening:

        st.success(
            "🟢 Microphone Active"
        )

        st.caption(
            "Listening for your response..."
        )

    else:

        st.warning(
            "⚪ Click 'Start Speaking' to answer."
        )

    # ------------------------------------------
    # Live Transcript
    # ------------------------------------------

    st.subheader(
        "📝 Live Speech Transcript"
    )

    st.caption(
        "Speech recognized in real time."
    )

    live_transcript = (
        audio_agent.get_transcript()
    )

    st.session_state.transcript = (
        live_transcript
    )

    st.text_area(

        "Live Transcript",

        value=live_transcript,

        height=180,

        disabled=False,

    )

    # ------------------------------------------
    # Voice Evaluation
    # ------------------------------------------

    if st.button(
        "✅ Submit Voice Answer"
    ):

        if not st.session_state.transcript.strip():

            st.warning(
                "Please speak before submitting."
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

                audio_agent.clear_transcript()

                st.session_state.transcript = ""

                st.session_state.live_listening = False

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
            
        session = (
            st.session_state.controller
            .interview_session
        )

        st.success(
            latest_evaluation["feedback"]
        )


    # --------------------------------------
    # Next Question
    # --------------------------------------
    session = (
            st.session_state.controller
            .interview_session
    )
    
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