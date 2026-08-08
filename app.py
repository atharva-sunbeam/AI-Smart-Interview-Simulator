import streamlit as st
import streamlit.components.v1 as components
import os
import time
from dotenv import load_dotenv, find_dotenv

# Auto-detect and load .env from current directory or parent workspace
load_dotenv(find_dotenv(usecwd=True))

from rag_pipeline.rag import RAGPipeline
from agents.resume_agent import ResumeAgent
from agents.orchestrator import SuperAgent, LLMManager
from agents.role_catalog import get_all_roles, get_role_blueprint
from frontend.audio_speaker import render_audio_speaker
from frontend.voice_input import render_voice_input_widget

# Page configuration
st.set_page_config(
    page_title="Smart AI Interview Simulator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Helper function to stop any active Speech Synthesis audio immediately
def cancel_active_speech():
    components.html(
        """
        <script>
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
        }
        </script>
        """,
        height=0,
        width=0
    )

# Initialize Session States
if "step" not in st.session_state:
    st.session_state.step = "home"
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "resume_name" not in st.session_state:
    st.session_state.resume_name = ""
if "parsed_skills" not in st.session_state:
    st.session_state.parsed_skills = []
if "parsed_domains" not in st.session_state:
    st.session_state.parsed_domains = {}
if "parsed_projects" not in st.session_state:
    st.session_state.parsed_projects = []
if "selected_role" not in st.session_state:
    st.session_state.selected_role = "Linux System Administrator"
if "selected_difficulty" not in st.session_state:
    st.session_state.selected_difficulty = "Easy"
if "interviewer_persona" not in st.session_state:
    st.session_state.interviewer_persona = "Alex"
if "auto_speak" not in st.session_state:
    st.session_state.auto_speak = True
if "questions" not in st.session_state:
    st.session_state.questions = []
if "current_q_idx" not in st.session_state:
    st.session_state.current_q_idx = 0
if "answered_questions" not in st.session_state:
    st.session_state.answered_questions = set()
if "history" not in st.session_state:
    st.session_state.history = []
if "in_followup" not in st.session_state:
    st.session_state.in_followup = False
if "followup_question" not in st.session_state:
    st.session_state.followup_question = ""
if "main_evaluation" not in st.session_state:
    st.session_state.main_evaluation = None
if "current_evaluation" not in st.session_state:
    st.session_state.current_evaluation = None
if "followup_evaluation" not in st.session_state:
    st.session_state.followup_evaluation = None
if "final_report" not in st.session_state:
    st.session_state.final_report = ""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0b0f19;
    color: #e2e8f0;
}

iframe {
    border: none !important;
    background: transparent !important;
}

div[data-testid="stCustomComponentV1"], div[data-testid="stCustomComponentV1"] > iframe, div[data-testid="stIFrame"], iframe[title*="voice"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

div[data-testid="stSkeleton"], .stCustomComponentSkeleton {
    display: none !important;
}

/* Hide Streamlit header anchor link symbols globally */
.main h1 a, .main h2 a, .main h3 a, .main h4 a, .main h5 a, .main h6 a,
a.anchor-link, [data-testid="stHeaderActionElements"], .header-anchor, a[title="Link to heading"] {
    display: none !important;
    visibility: hidden !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', sans-serif;
    color: #ffffff;
    font-weight: 600;
}

.glass-card {
    background: rgba(30, 41, 59, 0.45);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}

.premium-header {
    background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700;
}

.stButton>button {
    background: linear-gradient(90deg, #4f46e5 0%, #3b82f6 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 14px rgba(79, 70, 229, 0.4) !important;
}

.stButton>button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(79, 70, 229, 0.6) !important;
    background: linear-gradient(90deg, #4338ca 0%, #2563eb 100%) !important;
}

[data-testid="stSidebar"] {
    background-color: #0f172a;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}

.skill-badge {
    display: inline-block;
    background: rgba(6, 182, 212, 0.15);
    color: #06b6d4;
    border: 1px solid rgba(6, 182, 212, 0.3);
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 500;
    margin: 4px;
}

.project-card {
    background: rgba(168, 85, 247, 0.1);
    border: 1px solid rgba(168, 85, 247, 0.25);
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 14px;
}

.topic-badge-active {
    display: inline-block;
    background: rgba(79, 70, 229, 0.25);
    color: #818cf8;
    border: 1px solid #6366f1;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    margin: 4px;
}

.difficulty-badge-easy {
    background: rgba(16, 185, 129, 0.15);
    color: #10b981;
    border: 1px solid rgba(16, 185, 129, 0.3);
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 11px;
}
.difficulty-badge-medium {
    background: rgba(245, 158, 11, 0.15);
    color: #f59e0b;
    border: 1px solid rgba(245, 158, 11, 0.3);
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 11px;
}
.difficulty-badge-hard {
    background: rgba(244, 63, 94, 0.15);
    color: #f43f5e;
    border: 1px solid rgba(244, 63, 94, 0.3);
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 11px;
}

.score-badge {
    font-size: 24px;
    font-weight: 700;
    padding: 10px 20px;
    border-radius: 12px;
    display: inline-block;
    text-align: center;
}
.score-badge-high {
    background: rgba(16, 185, 129, 0.2);
    color: #10b981;
    border: 1px solid #10b981;
}
.score-badge-med {
    background: rgba(245, 158, 11, 0.2);
    color: #f59e0b;
    border: 1px solid #f59e0b;
}
.score-badge-low {
    background: rgba(244, 63, 94, 0.2);
    color: #f43f5e;
    border: 1px solid #f43f5e;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ----------------- PIPELINE INITIALIZATION -----------------

@st.cache_resource(show_spinner="Initializing AI Multi-Agent & RAG System...")
def get_pipeline():
    rag = RAGPipeline()
    rag.initialize_db(force_recreate=False)

    llm_manager = LLMManager()
    super_agent = SuperAgent(rag, llm_manager)
    resume_agent = ResumeAgent()

    return rag, llm_manager, super_agent, resume_agent

rag, llm_manager, super_agent, resume_agent = get_pipeline()

# ----------------- SIDEBAR CONSOLE -----------------
with st.sidebar:
    st.image("https://img.icons8.com/isometric/512/bot.png", width=70)
    st.markdown("### Interview Console")
    st.markdown("---")

    # Multi-Tier Engine Connection Status
    provider = super_agent.llm_manager.provider
    if provider == "groq":
        st.success("🤖 Engine: Groq API (llama-3.3-70b-versatile)")
    elif provider == "ollama":
        st.success("🤖 Engine: Ollama (Local Server)")
    else:
        st.info("💡 Engine: Smart Offline Heuristic")

    st.markdown("---")
    # Display Target Role & Stage ONLY after role selection or during active session/report
    if st.session_state.step in ["role_selection", "session", "feedback_report"]:
        st.markdown(f"**Target Role:**\n`{st.session_state.selected_role}`")
        st.markdown(f"**Strict Difficulty:**\n`{st.session_state.selected_difficulty}`")
        st.markdown(f"**Interviewer:**\n`{st.session_state.get('interviewer_persona', 'Alex')}`")
        if st.session_state.resume_name:
            st.markdown(f"**Resume parsed:**\n`{st.session_state.resume_name}`")

        if st.session_state.step == "session" and st.session_state.questions:
            q_num = st.session_state.current_q_idx + 1
            tot_q = len(st.session_state.questions)
            st.markdown(f"**Progress:**\n`Question {q_num} of {tot_q}`")

        st.markdown("---")
        if st.button("Reset Interview", use_container_width=True):
            cancel_active_speech()
            st.session_state.step = "home"
            st.session_state.resume_text = ""
            st.session_state.resume_name = ""
            st.session_state.parsed_skills = []
            st.session_state.parsed_domains = {}
            st.session_state.parsed_projects = []
            st.session_state.questions = []
            st.session_state.current_q_idx = 0
            st.session_state.answered_questions = set()
            st.session_state.history = []
            st.session_state.in_followup = False
            st.session_state.followup_question = ""
            st.session_state.main_evaluation = None
            st.session_state.current_evaluation = None
            st.session_state.followup_evaluation = None
            st.session_state.final_report = ""
            st.rerun()

# ----------------- MAIN FLOW PAGES -----------------

# Page 1: Home Landing Page
if st.session_state.step == "home":
    st.markdown("<h1 class='premium-header'>AI-Powered Smart Technical Interview Simulator</h1>", unsafe_allow_html=True)
    st.markdown("### Specialized Placement Preparation across 50+ Engineering Roles")
    st.write("")

    st.markdown(
        "<div class='glass-card'>"
        "<h4>Adaptive Blueprint Interview System</h4>"
        "<p>This agentic simulator provides topic-by-topic blueprint interviews tailored to 50+ engineering roles. "
        "It features strict fixed difficulty control (Easy/Medium/Hard), resume project & tool extraction, "
        "cross-session question non-repetition, independent follow-up evaluation, and real-time voice feedback. Built with LangChain, CrewAI, Groq LLM (llama-3.3-70b-versatile) & ChromaDB RAG.</p>"
        "</div>", 
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            "<div class='glass-card' style='height: 220px;'>"
            "<h5>📄 Precise Skill & Project Parsing</h5>"
            "<p style='font-size:14px; color:#cbd5e1;'>Parses uploaded resumes to extract exact skills, Project Names, specific tools, and short descriptions.</p>"
            "</div>", 
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            "<div class='glass-card' style='height: 220px;'>"
            "<h5>🎯 Strict Fixed Difficulty</h5>"
            "<p style='font-size:14px; color:#cbd5e1;'>Select Easy, Medium, or Hard to strictly enforce that difficulty throughout the entire session.</p>"
            "</div>", 
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            "<div class='glass-card' style='height: 220px;'>"
            "<h5>💡 Zero Cross-Session Repetition</h5>"
            "<p style='font-size:14px; color:#cbd5e1;'>Interview questions are tracked globally and guaranteed never to repeat across sessions.</p>"
            "</div>", 
            unsafe_allow_html=True
        )

    st.write("")
    st.write("")
    if st.button("Begin Preparation ->", type="primary"):
        st.session_state.step = "resume_upload"
        st.rerun()

# Page 2: Resume Upload
elif st.session_state.step == "resume_upload":
    st.markdown("<h2>Step 1: Upload Your Technical Resume</h2>", unsafe_allow_html=True)
    st.write("Our Resume Analyzer Agent extracts your exact skills and projects, automatically predicting your target job role.")

    uploaded_file = st.file_uploader("Upload PDF Resume", type=["pdf"])

    if uploaded_file is not None:
        temp_dir = "datasets/processed"
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, uploaded_file.name)

        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner("Analyzing resume content and predicting target job role..."):
            res = resume_agent.parse_resume(temp_path)

            st.session_state.resume_name = uploaded_file.name
            st.session_state.parsed_skills = res["skills"]
            st.session_state.parsed_domains = res["skills_by_domain"]
            st.session_state.parsed_projects = res["projects"]
            st.session_state.selected_role = res["recommended_role"]

            try:
                os.remove(temp_path)
            except Exception:
                pass

        st.success("🎉 Resume successfully parsed and accurately matched!")

        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### Extracted Skill & Project Matrices")
        st.markdown(f"**Predicted Target Role:** `{st.session_state.selected_role}`")
        st.write("")

        if st.session_state.parsed_domains:
            for domain, skills in st.session_state.parsed_domains.items():
                st.write(f"**{domain}:**")
                badges_html = "".join([f"<span class='skill-badge'>{skill}</span>" for skill in skills])
                st.markdown(badges_html, unsafe_allow_html=True)
                st.write("")

        if st.session_state.parsed_projects:
            st.markdown("#### Extracted Projects, Tools & Short Descriptions:")
            for proj in st.session_state.parsed_projects:
                if isinstance(proj, dict):
                    p_name = proj.get("name", "Project")
                    p_tools = proj.get("tools", [])
                    p_desc = proj.get("description", p_name)
                    tools_html = "".join([f"<span class='skill-badge'>{t}</span>" for t in p_tools])
                    st.markdown(
                        f"<div class='project-card'>"
                        f"📌 <strong>{p_name}</strong><br/>"
                        f"<span style='font-size:13px; color:#cbd5e1;'>{p_desc}</span><br/>"
                        f"<div style='margin-top:6px;'>Tools/Tech: {tools_html}</div>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(f"<div class='project-card'>📌 {proj}</div>", unsafe_allow_html=True)
            st.write("")

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    col_back, col_next = st.columns([1, 6])
    with col_back:
        if st.button("<- Back"):
            st.session_state.step = "home"
            st.rerun()
    with col_next:
        if st.session_state.resume_name:
            if st.button("Proceed to Role & Difficulty Settings ->"):
                st.session_state.step = "role_selection"
                st.rerun()
        else:
            st.info("Please upload a PDF resume to proceed, or click Skip below to configure settings manually.")
            if st.button("Skip / Custom Configuration"):
                st.session_state.step = "role_selection"
                st.rerun()

# Page 3: Role & Difficulty Selection
elif st.session_state.step == "role_selection":
    st.markdown("<h2>Step 2: Select Target Job Role & Difficulty Tier</h2>", unsafe_allow_html=True)
    st.write("Configure your interview parameters. The Question Engine will strictly enforce your chosen difficulty level.")

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

    all_roles = get_all_roles()
    default_role_idx = all_roles.index(st.session_state.selected_role) if st.session_state.selected_role in all_roles else 0

    difficulty_options = ["Easy", "Medium", "Hard"]
    default_diff_idx = difficulty_options.index(st.session_state.selected_difficulty) if st.session_state.selected_difficulty in difficulty_options else 0

    with st.form(key="role_selection_form"):
        selected_role = st.selectbox(
            "Select Target Job Role",
            all_roles,
            index=default_role_idx
        )

        selected_difficulty = st.selectbox(
            "Strict Fixed Difficulty Level (Will NOT change during session)",
            difficulty_options,
            index=default_diff_idx,
            help="Easy: Beginner/Definitions ONLY | Medium: Intermediate/Practical ONLY | Hard: System Design/Architecture ONLY"
        )

        persona_options = ["Alex", "Sophia", "Nexus"]
        persona_labels = {
            "Alex": "👨‍💼 Alex — Senior Lead Architect (Analytical & Direct)",
            "Sophia": "👩‍💼 Sophia — VP of Engineering (Warm & Encouraging)",
            "Nexus": "🤖 Nexus — Futuristic Tech Director (Cyberpunk & Precision)"
        }
        selected_persona = st.selectbox(
            "AI Interviewer Character Persona",
            persona_options,
            format_func=lambda x: persona_labels[x],
            index=persona_options.index(st.session_state.get("interviewer_persona", "Alex"))
        )

        auto_speak_val = st.checkbox(
            "🔊 Enable Real-Time Voice Audio (Auto-Speak Question & Feedback)",
            value=st.session_state.get("auto_speak", True)
        )

        q_count = st.slider("Number of Blueprint Questions (Selecting >5 includes resume project questions)", min_value=3, max_value=10, value=6)

        st.markdown("</div>", unsafe_allow_html=True)
        submit_btn = st.form_submit_button("Initialize Blueprint Interview ->")

    if submit_btn:
        st.session_state.selected_role = selected_role
        st.session_state.selected_difficulty = selected_difficulty
        st.session_state.interviewer_persona = selected_persona
        st.session_state.auto_speak = auto_speak_val
        st.session_state.q_count = q_count
        st.session_state.questions = []
        st.session_state.answered_questions = set()
        st.session_state.history = []
        st.session_state.current_q_idx = 0
        st.session_state.in_followup = False
        st.session_state.followup_question = ""
        st.session_state.main_evaluation = None
        st.session_state.current_evaluation = None
        st.session_state.followup_evaluation = None
        st.session_state.step = "session"
        st.rerun()

    col_back, _ = st.columns([1, 6])
    with col_back:
        if st.button("<- Back"):
            st.session_state.step = "resume_upload"
            st.rerun()

# Page 4: Active Interview Session Page
elif st.session_state.step == "session":
    # Synthesize questions if not yet loaded
    if not st.session_state.questions:
        with st.spinner("Synthesizing topic blueprint and question sequence using Groq API & Knowledge Base..."):
            questions = super_agent.get_questions(
                role=st.session_state.selected_role,
                difficulty=st.session_state.selected_difficulty,
                count=st.session_state.get("q_count", 6),
                skills=st.session_state.parsed_skills,
                projects=st.session_state.parsed_projects
            )
            st.session_state.questions = questions

        if len(st.session_state.questions) > 0:
            st.rerun()
        else:
            st.error("No questions could be generated matching selection parameters. Please check database content.")
            st.session_state.step = "role_selection"
            st.rerun()

    q_idx = st.session_state.current_q_idx
    total_q = len(st.session_state.questions)

    if q_idx >= total_q:
        cancel_active_speech()
        st.session_state.step = "feedback_report"
        st.rerun()

    current_q_data = st.session_state.questions[q_idx]
    # STRICT DIFFICULTY LOCK: Always keep selected difficulty level
    current_difficulty = st.session_state.selected_difficulty
    current_q_data["difficulty"] = current_difficulty

    # Determine speech text for auto-speak audio
    if not st.session_state.in_followup and st.session_state.current_evaluation is None:
        text_to_speak = f"Question {q_idx+1}. {current_q_data['question']}"
    elif st.session_state.in_followup and st.session_state.followup_evaluation is None:
        text_to_speak = f"Here is a follow-up question. {st.session_state.followup_question}"
    elif st.session_state.in_followup and st.session_state.followup_evaluation:
        score = st.session_state.followup_evaluation["score"]
        speech_feedback = st.session_state.followup_evaluation["feedback"].replace("*", "").replace("#", "").replace("`", "")
        text_to_speak = f"Follow-up score: {score} out of 10. {speech_feedback}"
    else:
        score = st.session_state.current_evaluation["score"]
        speech_feedback = st.session_state.current_evaluation["feedback"].replace("*", "").replace("#", "").replace("`", "")
        text_to_speak = f"You scored {score} out of 10. {speech_feedback}"

    # Active Blueprint Topic Progress Banner
    active_topic = current_q_data.get("topic", "General")

    st.markdown(
        f"<div class='glass-card'>"
        f"<h4>Question {q_idx+1} of {total_q}</h4>"
        f"<p style='font-size: 18px; color: #ffffff;'>{current_q_data['question']}</p>"
        f"<div style='margin-top: 10px;'>"
        f"Active Blueprint Topic: <span class='topic-badge-active'>{active_topic}</span> "
        f"Strict Difficulty: <span class='difficulty-badge-{current_difficulty.lower()}'>{current_difficulty}</span>"
        f"</div>"
        f"</div>",
        unsafe_allow_html=True
    )

    # Auto-speak Text-to-Speech audio speaker rendered AFTER Question card UI is on screen
    render_audio_speaker(
        text_to_speak=text_to_speak,
        auto_speak=st.session_state.get("auto_speak", True)
    )

    if st.session_state.in_followup:
        st.markdown(
            f"<div style='background: rgba(245, 158, 11, 0.1); border-left: 4px solid #f59e0b; padding: 16px; border-radius: 8px; margin-bottom: 20px;'>"
            f"⚠️ <strong>Follow-up Active:</strong> {st.session_state.followup_question}"
            f"</div>",
            unsafe_allow_html=True
        )

    input_key = f"answer_box_{q_idx}_{st.session_state.in_followup}"
    voice_key = f"voice_widget_{input_key}"

    # Render bi-directional Voice Recording component for hands-free speech input
    render_voice_input_widget(key=voice_key)

    label = "Your Answer to Main Question" if not st.session_state.in_followup else "Your Answer to Follow-up Question"
    user_ans = st.text_area(
        label,
        key=input_key,
        height=150,
        placeholder="Explain your answer in technical detail here (or click Record Voice Answer above to speak)..."
    )

    final_user_ans = user_ans.strip()

    # Display Standalone Main Question Evaluation
    if not st.session_state.in_followup and st.session_state.current_evaluation is None:
        if st.button("Submit Main Answer"):
            if not final_user_ans:
                st.warning("Please input an answer before submitting.")
            else:
                with st.spinner("Answer Evaluator Agent checking technical accuracy..."):
                    eval_res = super_agent.evaluate(
                        question=current_q_data["question"],
                        expected_answer=current_q_data["expected_answer"],
                        user_answer=final_user_ans
                    )
                    st.session_state.main_evaluation = {
                        "question": current_q_data["question"],
                        "topic": active_topic,
                        "score": eval_res["score"],
                        "feedback": eval_res["feedback"],
                        "user_answer": final_user_ans,
                        "is_followup": False
                    }
                    st.session_state.current_evaluation = st.session_state.main_evaluation
                st.rerun()

    # Display Standalone Follow-up Question Evaluation
    elif st.session_state.in_followup and st.session_state.followup_evaluation is None:
        if st.button("Submit Follow-up Answer"):
            if not final_user_ans:
                st.warning("Please input an answer before submitting.")
            else:
                with st.spinner("Answer Evaluator Agent evaluating follow-up response independently..."):
                    eval_res = super_agent.evaluate(
                        question=st.session_state.followup_question,
                        expected_answer=current_q_data["expected_answer"],
                        user_answer=final_user_ans
                    )
                    st.session_state.followup_evaluation = {
                        "question": st.session_state.followup_question,
                        "topic": active_topic,
                        "score": eval_res["score"],
                        "feedback": eval_res["feedback"],
                        "user_answer": final_user_ans,
                        "is_followup": True
                    }
                st.rerun()

    # Feedback Cards
    if not st.session_state.in_followup and st.session_state.current_evaluation:
        eval_data = st.session_state.current_evaluation
        score = eval_data["score"]
        score_class = "score-badge-high" if score >= 8.0 else ("score-badge-med" if score >= 5.0 else "score-badge-low")

        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### Main Question Feedback")
        st.markdown(f"<span class='score-badge {score_class}'>{score} / 10</span>", unsafe_allow_html=True)
        st.write("")
        st.markdown(eval_data["feedback"])
        st.markdown("</div>", unsafe_allow_html=True)

        col_fu, col_nxt = st.columns([1, 1])
        with col_fu:
            if st.button("❓ Ask Real-Time Follow-Up Question", use_container_width=True):
                st.session_state.in_followup = True
                with st.spinner("Follow-Up Agent generating real-time probing question..."):
                    st.session_state.followup_question = super_agent.generate_followup(
                        question=current_q_data["question"],
                        expected_answer=current_q_data["expected_answer"],
                        user_answer=st.session_state.main_evaluation["user_answer"],
                        role=st.session_state.selected_role,
                        difficulty=st.session_state.selected_difficulty
                    )
                st.rerun()

        with col_nxt:
            btn_label = "Proceed to Next Question ->" if q_idx + 1 < total_q else "Finish & View Final Report ->"
            if st.button(btn_label, use_container_width=True):
                cancel_active_speech()
                # Save main question evaluation to history
                if st.session_state.main_evaluation:
                    st.session_state.history.append({
                        "question": st.session_state.main_evaluation["question"],
                        "topic": st.session_state.main_evaluation["topic"],
                        "score": st.session_state.main_evaluation["score"],
                        "answer": st.session_state.main_evaluation["user_answer"],
                        "feedback": st.session_state.main_evaluation["feedback"],
                        "is_followup": False
                    })

                st.session_state.current_evaluation = None
                st.session_state.main_evaluation = None
                st.session_state.in_followup = False
                st.session_state.followup_question = ""
                st.session_state.followup_evaluation = None

                if q_idx + 1 < total_q:
                    st.session_state.current_q_idx += 1
                    st.rerun()
                else:
                    st.session_state.step = "feedback_report"
                    with st.spinner("Feedback Agent compiling diagnostic report & updating system memory..."):
                        report = super_agent.generate_report(
                            role=st.session_state.selected_role,
                            history=st.session_state.history
                        )
                        st.session_state.final_report = report
                    st.rerun()

    elif st.session_state.in_followup and st.session_state.followup_evaluation:
        eval_data = st.session_state.followup_evaluation
        score = eval_data["score"]
        score_class = "score-badge-high" if score >= 8.0 else ("score-badge-med" if score >= 5.0 else "score-badge-low")

        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### Standalone Follow-up Feedback")
        st.markdown(f"<span class='score-badge {score_class}'>{score} / 10</span>", unsafe_allow_html=True)
        st.write("")
        st.markdown(eval_data["feedback"])
        st.markdown("</div>", unsafe_allow_html=True)

        btn_label = "Proceed to Next Question ->" if q_idx + 1 < total_q else "Finish & View Final Report ->"
        if st.button(btn_label, use_container_width=True):
            cancel_active_speech()
            # Save both main and follow-up evaluations as distinct entries
            if st.session_state.main_evaluation:
                st.session_state.history.append({
                    "question": st.session_state.main_evaluation["question"],
                    "topic": st.session_state.main_evaluation["topic"],
                    "score": st.session_state.main_evaluation["score"],
                    "answer": st.session_state.main_evaluation["user_answer"],
                    "feedback": st.session_state.main_evaluation["feedback"],
                    "is_followup": False
                })

            st.session_state.history.append({
                "question": st.session_state.followup_evaluation["question"],
                "topic": st.session_state.followup_evaluation["topic"],
                "score": st.session_state.followup_evaluation["score"],
                "answer": st.session_state.followup_evaluation["user_answer"],
                "feedback": st.session_state.followup_evaluation["feedback"],
                "is_followup": True
            })

            st.session_state.current_evaluation = None
            st.session_state.main_evaluation = None
            st.session_state.in_followup = False
            st.session_state.followup_question = ""
            st.session_state.followup_evaluation = None

            if q_idx + 1 < total_q:
                st.session_state.current_q_idx += 1
                st.rerun()
            else:
                st.session_state.step = "feedback_report"
                with st.spinner("Feedback Agent compiling diagnostic report & updating system memory..."):
                    report = super_agent.generate_report(
                        role=st.session_state.selected_role,
                        history=st.session_state.history
                    )
                    st.session_state.final_report = report
                st.rerun()

# Page 5: Feedback Report & Diagnostic Evaluation
elif st.session_state.step == "feedback_report":
    cancel_active_speech()

    st.markdown("<h2 class='premium-header'>Interview Evaluation & Self-Learning Report</h2>", unsafe_allow_html=True)
    st.write("Congratulations on completing your technical interview session! Below is your comprehensive diagnostic feedback.")

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown(st.session_state.final_report)
    st.markdown("</div>", unsafe_allow_html=True)

    st.download_button(
        label="📥 Download Markdown Report",
        data=st.session_state.final_report,
        file_name=f"interview_report_{st.session_state.selected_role.replace(' ', '_').lower()}.md",
        mime="text/markdown",
        use_container_width=True
    )

    st.write("")
    if st.button("Start a New Session"):
        cancel_active_speech()
        st.session_state.step = "home"
        st.session_state.resume_text = ""
        st.session_state.resume_name = ""
        st.session_state.parsed_skills = []
        st.session_state.parsed_domains = {}
        st.session_state.parsed_projects = []
        st.session_state.questions = []
        st.session_state.current_q_idx = 0
        st.session_state.answered_questions = set()
        st.session_state.history = []
        st.session_state.in_followup = False
        st.session_state.followup_question = ""
        st.session_state.main_evaluation = None
        st.session_state.current_evaluation = None
        st.session_state.followup_evaluation = None
        st.session_state.final_report = ""
        st.rerun()
