import streamlit as st
import os
import time
from rag_pipeline.rag import RAGPipeline
from agents.resume_agent import ResumeAgent
from agents.orchestrator import OllamaClient, QuestionGeneratorAgent, AnswerEvaluatorAgent, FollowUpAgent, FeedbackAgent

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
if "current_evaluation" not in st.session_state:
    st.session_state.current_evaluation = None
if "final_report" not in st.session_state:
    st.session_state.final_report = ""

# Load Custom Styles
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Inter:wght@300;400;500;600&display=swap');

/* Global Font Configurations */
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

/* Glassmorphic Cards styling */
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

/* Dynamic Buttons */
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

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: #0f172a;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}

/* Skill tags */
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

/* Evaluation Score Badge */
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

@st.cache_resource
def get_pipeline():
    rag = RAGPipeline()
    # Lazy initialisation: build if not exists
    rag.initialize_db(force_recreate=False)
    
    ollama_client = OllamaClient()
    
    resume_agent = ResumeAgent()
    qgen_agent = QuestionGeneratorAgent(rag, ollama_client)
    eval_agent = AnswerEvaluatorAgent(ollama_client)
    followup_agent = FollowUpAgent(ollama_client)
    feedback_agent = FeedbackAgent(ollama_client)
    
    return resume_agent, qgen_agent, eval_agent, followup_agent, feedback_agent

resume_agent, qgen_agent, eval_agent, followup_agent, feedback_agent = get_pipeline()

# ----------------- SIDEBAR STATUS -----------------
with st.sidebar:
    st.image("https://img.icons8.com/isometric/512/bot.png", width=70)
    st.markdown("### Interview Console")
    st.markdown("---")
    
    # Show connection status
    client = OllamaClient()
    if client.is_connected:
        st.success("🤖 Ollama: ONLINE (mistral)")
    else:
        st.info("💡 Mode: OFFLINE (Simulated)")
        
    st.markdown("---")
    # Show progress or session status
    if st.session_state.step != "home":
        st.markdown(f"**Target Role:**\n`{st.session_state.selected_role}`")
        st.markdown(f"**Difficulty:**\n`{st.session_state.selected_difficulty}`")
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
            st.session_state.current_evaluation = None
            st.session_state.final_report = ""
            st.rerun()

# ----------------- MAIN FLOW PAGES -----------------

# Page 1: Home Landing Page
if st.session_state.step == "home":
    st.markdown("<h1 class='premium-header'>AI-Powered Technical Interview Simulator</h1>", unsafe_allow_html=True)
    st.markdown("### Accelerate Placement Preparation using RAG & Multi-Agent AI Architecture")
    st.write("")
    
    st.markdown(
        "<div class='glass-card'>"
        "<h4>Welcome to the Next-Generation Smart Interview System</h4>"
        "<p>This agentic simulator conducts rigorous technical interviews tailored to your resume, evaluates your answers in real-time, "
        "asks contextual follow-ups, and delivers a downloadable diagnostic performance report. Uses local vector databases and LLM validation.</p>"
        "</div>", 
        unsafe_allow_html=True
    )
    
    # Feature Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            "<div class='glass-card' style='height: 220px;'>"
            "<h5>📄 Resume-Driven Context</h5>"
            "<p style='font-size:14px; color:#cbd5e1;'>Parses uploaded resumes, extracts technical skill matrices, and configures target role questions.</p>"
            "</div>", 
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            "<div class='glass-card' style='height: 220px;'>"
            "<h5>🔍 RAG-Augmented Questions</h5>"
            "<p style='font-size:14px; color:#cbd5e1;'>Queries ChromaDB semantic indexes to retrieve topic-accurate interview questions based on your profile.</p>"
            "</div>", 
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            "<div class='glass-card' style='height: 220px;'>"
            "<h5>🧠 Multi-Agent Orchestrator</h5>"
            "<p style='font-size:14px; color:#cbd5e1;'>Logical agents specialize in question generation, answer scoring, and generating deep-dive follow-up triggers.</p>"
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
    st.write("Our Resume Analysis Agent extracts key technologies and matches them against target profiles.")
    
    uploaded_file = st.file_uploader("Upload PDF Resume", type=["pdf"])
    
    if uploaded_file is not None:
        # Save temporary file
        temp_dir = "datasets/processed"
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, uploaded_file.name)
        
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        with st.spinner("Analyzing resume content..."):
            # Execute resume parser
            res = resume_agent.parse_resume(temp_path)
            
            # Save variables
            st.session_state.resume_name = uploaded_file.name
            st.session_state.parsed_skills = res["skills"]
            st.session_state.parsed_domains = res["skills_by_domain"]
            st.session_state.selected_role = res["recommended_role"]
            
            # Clean up temp file
            try:
                os.remove(temp_path)
            except Exception:
                pass
                
        st.success("🎉 Resume successfully parsed and analyzed!")
        
        # Skill Matrices Display
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
            st.info("Please upload a PDF resume to proceed, or click Skip below to skip parsing.")
            if st.button("Skip / Custom Configuration"):
                st.session_state.step = "role_selection"
                st.rerun()

# Page 3: Role & Difficulty Selection
elif st.session_state.step == "role_selection":
    st.markdown("<h2>Step 2: Select Job Profile & Difficulty</h2>", unsafe_allow_html=True)
    st.write("Configure your simulator parameters. RAG pipelines will build questions fitting these settings.")
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    role_options = ["Python Developer", "Data Analyst", "Data Engineer", "Machine Learning Engineer"]
    default_role_idx = role_options.index(st.session_state.selected_role) if st.session_state.selected_role in role_options else 0
    
    selected_role = st.selectbox(
        "Target Role Profile",
        role_options,
        index=default_role_idx
    )
    
    difficulty_options = ["Easy", "Medium", "Hard"]
    default_diff_idx = difficulty_options.index(st.session_state.selected_difficulty)
    selected_difficulty = st.selectbox(
        "Interview Difficulty Tier",
        difficulty_options,
        index=default_diff_idx
    )
    
    q_count = st.slider("Number of Technical Questions", min_value=3, max_value=8, value=5)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.session_state.selected_role = selected_role
    st.session_state.selected_difficulty = selected_difficulty
    
    col_back, col_next = st.columns([1, 6])
    with col_back:
        if st.button("<- Back"):
            st.session_state.step = "resume_upload"
            st.rerun()
    with col_next:
        if st.button("Initialize Simulator Session ->"):
            with st.spinner("Retrieving target question sets from RAG database..."):
                # Fetch questions using QuestionGenerator
                st.session_state.questions = []
                st.session_state.answered_questions = set()
                st.session_state.history = []
                st.session_state.current_q_idx = 0
                st.session_state.in_followup = False
                st.session_state.current_evaluation = None
                
                # Retrieve questions from database
                temp_questions = []
                for _ in range(q_count):
                    q_data = qgen_agent.generate_question(
                        role=selected_role,
                        difficulty=selected_difficulty,
                        answered_questions=st.session_state.answered_questions,
                        skills=st.session_state.parsed_skills
                    )
                    if q_data:
                        temp_questions.append(q_data)
                        st.session_state.answered_questions.add(q_data["raw_question"])
                
                st.session_state.questions = temp_questions
                
            if len(st.session_state.questions) > 0:
                st.session_state.step = "session"
                st.rerun()
            else:
                st.error("No questions found in database matching selection parameters. Please re-run data collection.")

# Page 4: Interactive Interview Session
elif st.session_state.step == "session":
    # Progress calculations
    q_idx = st.session_state.current_q_idx
    questions = st.session_state.questions
    total_q = len(questions)
    
    st.markdown(f"<h2>Technical Interview Session ({q_idx+1}/{total_q})</h2>", unsafe_allow_html=True)
    
    # Progress Bar
    st.progress((q_idx) / total_q)
    
    # Main Question Card
    current_q_data = questions[q_idx]
    
    # Card layout
    st.markdown(
        f"<div class='glass-card'>"
        f"<h4>Question {q_idx+1}</h4>"
        f"<p style='font-size: 18px; color: #ffffff;'>{current_q_data['question']}</p>"
        f"<span class='skill-badge'>{current_q_data['topic']}</span>"
        f"<span class='difficulty-badge-{current_q_data['difficulty'].lower()}'>{current_q_data['difficulty']}</span>"
        f"</div>",
        unsafe_allow_html=True
    )
    
    # Follow-up trigger notification
    if st.session_state.in_followup:
        st.markdown(
            f"<div style='background: rgba(245, 158, 11, 0.1); border-left: 4px solid #f59e0b; padding: 16px; border-radius: 8px; margin-bottom: 20px;'>"
            f"⚠️ <strong>Follow-up Active:</strong> {st.session_state.followup_question}"
            f"</div>",
            unsafe_allow_html=True
        )

    # Text Input for Candidate Answer
    label = "Your Answer" if not st.session_state.in_followup else "Your Answer to Follow-up"
    user_ans = st.text_area(label, height=150, placeholder="Explain your answer in technical detail here. Mention architectural patterns, keywords, or examples...")
    
    # Controls
    if st.session_state.current_evaluation is None:
        if st.button("Submit Answer"):
            if user_ans.strip() == "":
                st.warning("Please input an answer before submitting.")
            else:
                with st.spinner("Answer Evaluation Agent checking correctness..."):
                    # Process Answer
                    if not st.session_state.in_followup:
                        # Grade main question
                        eval_res = eval_agent.evaluate_answer(
                            question=current_q_data["question"],
                            expected_answer=current_q_data["expected_answer"],
                            user_answer=user_ans
                        )
                        st.session_state.current_evaluation = {
                            "main_score": eval_res["score"],
                            "main_feedback": eval_res["feedback"],
                            "main_answer": user_ans,
                            "final_score": eval_res["score"],
                            "final_feedback": eval_res["feedback"]
                        }
                    else:
                        # Grade follow-up question
                        eval_res = eval_agent.evaluate_answer(
                            question=st.session_state.followup_question,
                            expected_answer=current_q_data["expected_answer"],
                            user_answer=user_ans
                        )
                        
                        # Calculate final score as average of main and follow-up
                        main_score = st.session_state.current_evaluation["main_score"]
                        final_score = round((main_score + eval_res["score"]) / 2, 1)
                        
                        st.session_state.current_evaluation["followup_score"] = eval_res["score"]
                        st.session_state.current_evaluation["followup_answer"] = user_ans
                        st.session_state.current_evaluation["final_score"] = final_score
                        st.session_state.current_evaluation["final_feedback"] = (
                            f"**Main Question Feedback:** {st.session_state.current_evaluation['main_feedback']}\n\n"
                            f"**Follow-up Question Feedback:** {eval_res['feedback']}"
                        )
                st.rerun()
    else:
        # Display Evaluation Feedback
        eval_data = st.session_state.current_evaluation
        score = eval_data["final_score"]
        
        score_class = "score-badge-high" if score >= 8.0 else ("score-badge-med" if score >= 5.0 else "score-badge-low")
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### Answer Feedback")
        st.markdown(f"<span class='score-badge {score_class}'>{score} / 10</span>", unsafe_allow_html=True)
        st.write("")
        st.markdown(eval_data["final_feedback"])
        st.markdown("</div>", unsafe_allow_html=True)

        # Trigger Next step controls
        if not st.session_state.in_followup and 4.0 <= score <= 7.0:
            # Trigger Follow-Up question!
            st.info("💡 Your score triggered a follow-up question. This is an opportunity to expand on your explanation and improve your grade.")
            if st.button("Trigger Follow-Up Question"):
                st.session_state.in_followup = True
                # Generate follow-up
                with st.spinner("Generating follow-up question..."):
                    st.session_state.followup_question = followup_agent.generate_followup(
                        question=current_q_data["question"],
                        expected_answer=current_q_data["expected_answer"],
                        user_answer=eval_data["main_answer"]
                    )
                st.session_state.current_evaluation = None
                st.rerun()
                
        # Normal proceed controls
        if st.button("Proceed"):
            # Log question history
            st.session_state.history.append({
                "question": current_q_data["question"],
                "topic": current_q_data["topic"],
                "score": eval_data["final_score"],
                "answer": eval_data["main_answer"],
                "feedback": eval_data["final_feedback"]
            })
            
            # Reset page evaluation
            st.session_state.current_evaluation = None
            st.session_state.in_followup = False
            st.session_state.followup_question = ""
            
            if q_idx + 1 < total_q:
                st.session_state.current_q_idx += 1
                st.rerun()
            else:
                # Finished all questions!
                st.session_state.step = "feedback_report"
                with st.spinner("Feedback Agent compiling report..."):
                    # Generate report
                    report = feedback_agent.generate_report(
                        role=st.session_state.selected_role,
                        history=st.session_state.history
                    )
                    st.session_state.final_report = report
                st.rerun()

# Page 5: Feedback Report
elif st.session_state.step == "feedback_report":
    st.markdown("<h2 class='premium-header'>Interview Evaluation Report</h2>", unsafe_allow_html=True)
    st.write("Congratulations on completing your technical interview session! Here is your diagnostic feedback.")
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown(st.session_state.final_report)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Download report button
    st.download_button(
        label="📥 Download Markdown Report",
        data=st.session_state.final_report,
        file_name=f"interview_report_{st.session_state.selected_role.replace(' ', '_').lower()}.md",
        mime="text/markdown",
        use_container_width=True
    )
    
    st.write("")
    if st.button("Start a New Session"):
        # Reset variables
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
        st.session_state.current_evaluation = None
        st.session_state.final_report = ""
        st.rerun()
