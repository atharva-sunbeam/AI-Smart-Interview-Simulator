import streamlit as st
import os
import time
from dotenv import load_dotenv, find_dotenv

# Auto-detect and load .env from current directory or parent workspace
load_dotenv(find_dotenv(usecwd=True))

from rag_pipeline.rag import RAGPipeline
from agents.resume_agent import ResumeAgent
from agents.orchestrator import SuperAgent, LLMManager

# Page configuration
st.set_page_config(
    page_title="Smart AI Interview Simulator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
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
if "selected_role" not in st.session_state:
    st.session_state.selected_role = "Python Developer"
if "selected_difficulty" not in st.session_state:
    st.session_state.selected_difficulty = "Medium"
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
if "final_report" not in st.session_state:
    st.session_state.final_report = ""

TARGET_ROLES = [
    "Python Developer",
    "Data Analyst",
    "Data Engineer",
    "Machine Learning Engineer",
    "DevOps / Cloud Engineer",
    "Full Stack Developer",
    "Backend Engineer",
    "AI / LLM Engineer"
]

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0b0f19;
    color: #e2e8f0;
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
    
    return super_agent, resume_agent

super_agent, resume_agent = get_pipeline()

# ----------------- SIDEBAR CONSOLE -----------------
with st.sidebar:
    st.image("https://img.icons8.com/isometric/512/bot.png", width=70)
    st.markdown("### Interview Console")
    st.markdown("---")

    # Multi-Tier Engine Connection Status
    provider = super_agent.llm_manager.provider
    if provider == "grok":
        st.success("🤖 Engine: GROK API (Online)")
    elif provider == "groq":
        st.success("🤖 Engine: GROQ API (Online)")
    elif provider == "ollama":
        st.success("🤖 Engine: Ollama (Local Server)")
    else:
        st.info("💡 Engine: Smart Offline Heuristic")
        
    st.markdown("---")
    # Display Target Role & Stage ONLY after role selection or during active session/report
    if st.session_state.step in ["role_selection", "session", "feedback_report"]:
        st.markdown(f"**Target Role:**\n`{st.session_state.selected_role}`")
        st.markdown(f"**Current Stage:**\n`{st.session_state.selected_difficulty}`")
        if st.session_state.resume_name:
            st.markdown(f"**Resume parsed:**\n`{st.session_state.resume_name}`")
            
        if st.session_state.step == "session" and st.session_state.questions:
            q_num = st.session_state.current_q_idx + 1
            tot_q = len(st.session_state.questions)
            st.markdown(f"**Progress:**\n`Question {q_num} of {tot_q}`")
            
        st.markdown("---")
        if st.button("Reset Interview", use_container_width=True):
            st.session_state.step = "home"
            st.session_state.resume_text = ""
            st.session_state.resume_name = ""
            st.session_state.parsed_skills = []
            st.session_state.parsed_domains = {}
            st.session_state.questions = []
            st.session_state.current_q_idx = 0
            st.session_state.answered_questions = set()
            st.session_state.history = []
            st.session_state.in_followup = False
            st.session_state.followup_question = ""
            st.session_state.main_evaluation = None
            st.session_state.current_evaluation = None
            st.session_state.final_report = ""
            st.rerun()

# ----------------- MAIN FLOW PAGES -----------------

# Page 1: Home Landing Page
if st.session_state.step == "home":
    st.markdown("<h1 class='premium-header'>AI-Powered Technical Interview Simulator</h1>", unsafe_allow_html=True)
    st.markdown("### Accelerate Placement Preparation using RAG, Grok LLM & CrewAI Multi-Agent Architecture")
    st.write("")
    
    st.markdown(
        "<div class='glass-card'>"
        "<h4>Welcome to the Adaptive Multi-Agent Technical Interview Platform</h4>"
        "<p>This agentic simulator generates real-time technical interview questions using Grok & RAG (ChromaDB), "
        "evaluates your answers dynamically, asks probing follow-ups, adapts interview stage difficulty based on your ongoing performance, "
        "and enriches system memory continuously. Built with CrewAI, LangChain v1, and Streamlit.</p>"
        "</div>", 
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            "<div class='glass-card' style='height: 220px;'>"
            "<h5>📄 Resume & Profile Matching</h5>"
            "<p style='font-size:14px; color:#cbd5e1;'>Parses uploaded resumes, extracts technical skill matrices across 8 specialization tracks.</p>"
            "</div>", 
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            "<div class='glass-card' style='height: 220px;'>"
            "<h5>⚡ Real-Time Question Generation</h5>"
            "<p style='font-size:14px; color:#cbd5e1;'>Uses Grok & ChromaDB RAG context to synthesize unique, non-repetitive interview questions live.</p>"
            "</div>", 
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            "<div class='glass-card' style='height: 220px;'>"
            "<h5>🧠 CrewAI Agent System</h5>"
            "<p style='font-size:14px; color:#cbd5e1;'>Specialized CrewAI agents handle question generation, grading, follow-ups, and self-learning store updates.</p>"
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
    st.write("Our Resume Analysis Agent extracts key technologies and matches them against target engineering profiles.")
    
    uploaded_file = st.file_uploader("Upload PDF Resume", type=["pdf"])
    
    if uploaded_file is not None:
        temp_dir = "datasets/processed"
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, uploaded_file.name)
        
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        with st.spinner("Analyzing resume content..."):
            res = resume_agent.parse_resume(temp_path)
            
            st.session_state.resume_name = uploaded_file.name
            st.session_state.parsed_skills = res["skills"]
            st.session_state.parsed_domains = res["skills_by_domain"]
            st.session_state.selected_role = res["recommended_role"]
            
            try:
                os.remove(temp_path)
            except Exception:
                pass
                
        st.success("🎉 Resume successfully parsed and analyzed!")
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### Extracted Skill Matrices")
        st.markdown(f"**Recommended Target Profile:** `{st.session_state.selected_role}`")
        st.write("")
        
        if st.session_state.parsed_domains:
            for domain, skills in st.session_state.parsed_domains.items():
                st.write(f"**{domain}:**")
                badges_html = "".join([f"<span class='skill-badge'>{skill}</span>" for skill in skills])
                st.markdown(badges_html, unsafe_allow_html=True)
                st.write("")
        else:
            st.write("No distinct matching skill categories found. You can proceed with custom role settings.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.write("")
    col_back, col_next = st.columns([1, 6])
    with col_back:
        if st.button("<- Back"):
            st.session_state.step = "home"
            st.rerun()
    with col_next:
        if st.session_state.resume_name:
            if st.button("Proceed to Role Settings ->"):
                st.session_state.step = "role_selection"
                st.rerun()
        else:
            st.info("Please upload a PDF resume to proceed, or click Skip below to configure settings manually.")
            if st.button("Skip / Custom Configuration"):
                st.session_state.step = "role_selection"
                st.rerun()

# Page 3: Role & Difficulty Selection
elif st.session_state.step == "role_selection":
    st.markdown("<h2>Step 2: Select Job Profile & Difficulty Tier</h2>", unsafe_allow_html=True)
    st.write("Configure your interview parameters. Real-time RAG & Grok pipelines will synthesize questions for these settings.")
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    
    default_role_idx = TARGET_ROLES.index(st.session_state.selected_role) if st.session_state.selected_role in TARGET_ROLES else 0
    difficulty_options = ["Easy", "Medium", "Hard"]
    default_diff_idx = difficulty_options.index(st.session_state.selected_difficulty) if st.session_state.selected_difficulty in difficulty_options else 1
    
    with st.form(key="role_selection_form"):
        selected_role = st.selectbox(
            "Target Role Profile (8 Specialized Tracks)",
            TARGET_ROLES,
            index=default_role_idx
        )
        
        selected_difficulty = st.selectbox(
            "Initial Difficulty Tier",
            difficulty_options,
            index=default_diff_idx
        )
        
        q_count = st.slider("Number of Technical Questions", min_value=3, max_value=8, value=5)
        
        st.markdown("</div>", unsafe_allow_html=True)
        submit_btn = st.form_submit_button("Initialize Simulator Session ->")
    
    if submit_btn:
        st.session_state.selected_role = selected_role
        st.session_state.selected_difficulty = selected_difficulty
        
        with st.spinner("Synthesizing real-time question sets using Grok & ChromaDB RAG..."):
            st.session_state.questions = []
            st.session_state.answered_questions = set()
            st.session_state.history = []
            st.session_state.current_q_idx = 0
            st.session_state.in_followup = False
            st.session_state.followup_question = ""
            st.session_state.main_evaluation = None
            st.session_state.current_evaluation = None
            
            questions = super_agent.get_questions(
                role=selected_role,
                difficulty=selected_difficulty,
                count=q_count,
                skills=st.session_state.parsed_skills
            )
            st.session_state.questions = questions
            
        if len(st.session_state.questions) > 0:
            st.session_state.step = "session"
            st.rerun()
        else:
            st.error("No questions could be generated matching selection parameters. Please check database content.")

    col_back, _ = st.columns([1, 6])
    with col_back:
        if st.button("<- Back"):
            st.session_state.step = "resume_upload"
            st.rerun()

# Page 4: Interactive Interview Session
elif st.session_state.step == "session":
    q_idx = st.session_state.current_q_idx
    questions = st.session_state.questions
    total_q = len(questions)
    
    st.markdown(f"<h2>Technical Interview Session ({q_idx+1}/{total_q})</h2>", unsafe_allow_html=True)
    st.progress((q_idx) / total_q)
    
    current_q_data = questions[q_idx]
    # Synchronize difficulty badge on question card with active interview stage
    current_difficulty = st.session_state.selected_difficulty
    current_q_data["difficulty"] = current_difficulty
    
    st.markdown(
        f"<div class='glass-card'>"
        f"<h4>Question {q_idx+1}</h4>"
        f"<p style='font-size: 18px; color: #ffffff;'>{current_q_data['question']}</p>"
        f"<span class='skill-badge'>{current_q_data['topic']}</span>"
        f"<span class='difficulty-badge-{current_difficulty.lower()}'>{current_difficulty}</span>"
        f"</div>",
        unsafe_allow_html=True
    )
    
    if st.session_state.in_followup:
        st.markdown(
            f"<div style='background: rgba(245, 158, 11, 0.1); border-left: 4px solid #f59e0b; padding: 16px; border-radius: 8px; margin-bottom: 20px;'>"
            f"⚠️ <strong>Follow-up Active:</strong> {st.session_state.followup_question}"
            f"</div>",
            unsafe_allow_html=True
        )

    input_key = f"answer_box_{q_idx}_{st.session_state.in_followup}"
    label = "Your Answer" if not st.session_state.in_followup else "Your Answer to Follow-up"
    user_ans = st.text_area(label, key=input_key, height=150, placeholder="Explain your answer in technical detail here...")
    
    if st.session_state.current_evaluation is None:
        if st.button("Submit Answer"):
            if user_ans.strip() == "":
                st.warning("Please input an answer before submitting.")
            else:
                with st.spinner("Answer Evaluator Agent checking technical accuracy..."):
                    if not st.session_state.in_followup:
                        eval_res = super_agent.evaluate(
                            question=current_q_data["question"],
                            expected_answer=current_q_data["expected_answer"],
                            user_answer=user_ans
                        )
                        st.session_state.main_evaluation = {
                            "main_score": eval_res["score"],
                            "main_feedback": eval_res["feedback"],
                            "main_answer": user_ans
                        }
                        st.session_state.current_evaluation = {
                            "final_score": eval_res["score"],
                            "final_feedback": eval_res["feedback"]
                        }
                    else:
                        eval_res = super_agent.evaluate(
                            question=st.session_state.followup_question,
                            expected_answer=current_q_data["expected_answer"],
                            user_answer=user_ans
                        )
                        
                        main_score = st.session_state.main_evaluation["main_score"] if st.session_state.main_evaluation else 5.0
                        main_feedback = st.session_state.main_evaluation["main_feedback"] if st.session_state.main_evaluation else ""
                        final_score = round((main_score + eval_res["score"]) / 2, 1)
                        
                        st.session_state.current_evaluation = {
                            "followup_score": eval_res["score"],
                            "followup_answer": user_ans,
                            "final_score": final_score,
                            "final_feedback": (
                                f"**Main Question Feedback:** {main_feedback}\n\n"
                                f"**Follow-up Feedback:** {eval_res['feedback']}"
                            )
                        }
                st.rerun()
    else:
        eval_data = st.session_state.current_evaluation
        score = eval_data["final_score"]
        
        score_class = "score-badge-high" if score >= 8.0 else ("score-badge-med" if score >= 5.0 else "score-badge-low")
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### Answer Feedback")
        st.markdown(f"<span class='score-badge {score_class}'>{score} / 10</span>", unsafe_allow_html=True)
        st.write("")
        st.markdown(eval_data["final_feedback"])
        st.markdown("</div>", unsafe_allow_html=True)

        col_fu, col_nxt = st.columns([1, 1])
        
        # Follow-Up Question Option (Available if not already in follow-up)
        if not st.session_state.in_followup:
            with col_fu:
                if st.button("❓ Ask Real-Time Follow-Up Question", use_container_width=True):
                    st.session_state.in_followup = True
                    with st.spinner("Follow-Up Agent generating real-time probing question..."):
                        main_ans = st.session_state.main_evaluation["main_answer"] if st.session_state.main_evaluation else user_ans
                        st.session_state.followup_question = super_agent.generate_followup(
                            question=current_q_data["question"],
                            expected_answer=current_q_data["expected_answer"],
                            user_answer=main_ans,
                            role=st.session_state.selected_role
                        )
                    st.session_state.current_evaluation = None
                    st.rerun()

        with col_nxt:
            btn_label = "Proceed to Next Question ->" if q_idx + 1 < total_q else "Finish & View Final Report ->"
            if st.button(btn_label, use_container_width=True):
                main_ans = st.session_state.main_evaluation["main_answer"] if st.session_state.main_evaluation else ""
                st.session_state.history.append({
                    "question": current_q_data["question"],
                    "topic": current_q_data["topic"],
                    "score": eval_data["final_score"],
                    "answer": main_ans,
                    "feedback": eval_data["final_feedback"]
                })
                
                st.session_state.current_evaluation = None
                st.session_state.main_evaluation = None
                st.session_state.in_followup = False
                st.session_state.followup_question = ""
                
                st.session_state.selected_difficulty = super_agent.get_adaptive_difficulty(
                    st.session_state.selected_difficulty,
                    st.session_state.history
                )
                
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
        st.session_state.step = "home"
        st.session_state.resume_text = ""
        st.session_state.resume_name = ""
        st.session_state.parsed_skills = []
        st.session_state.parsed_domains = {}
        st.session_state.questions = []
        st.session_state.current_q_idx = 0
        st.session_state.answered_questions = set()
        st.session_state.history = []
        st.session_state.in_followup = False
        st.session_state.followup_question = ""
        st.session_state.main_evaluation = None
        st.session_state.current_evaluation = None
        st.session_state.final_report = ""
        st.rerun()
