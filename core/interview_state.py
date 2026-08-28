import uuid
import time
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class InterviewState(BaseModel):
    """
    Centralized State Model for the AI Smart Interview Simulator.
    Stores session metadata, conversation history, resume context, 
    RAG findings, evaluations, decisions, and framework debug execution logs.
    """
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    candidate_name: str = "Candidate"
    target_role: str = "Linux System Administrator"
    difficulty: str = "Easy"
    interviewer_persona: str = "Alex"
    auto_speak: bool = True
    
    current_phase: str = "home"  # home, resume_upload, role_selection, session, feedback_report
    current_question_index: int = 0
    main_question_count: int = 6
    main_questions_asked: int = 0
    follow_up_count: int = 0
    total_questions_target: int = 6
    
    current_question: str = ""
    current_expected_answer: str = ""
    current_topic: str = ""
    in_followup: bool = False
    followup_question: str = ""
    
    transcript: List[Dict[str, Any]] = Field(default_factory=list)
    asked_questions: List[str] = Field(default_factory=list)
    
    # Resume context extracted from PDF
    resume_context: Dict[str, Any] = Field(default_factory=lambda: {
        "skills": [],
        "skills_by_domain": {},
        "projects": [],
        "recommended_role": ""
    })
    
    retrieved_context: List[Dict[str, Any]] = Field(default_factory=list)
    evaluations: List[Dict[str, Any]] = Field(default_factory=list)
    previous_evaluation: Optional[Dict[str, Any]] = None
    interview_decisions: List[Dict[str, Any]] = Field(default_factory=list)
    
    final_report: str = ""
    
    # Live framework execution observability log (for Viva / Developer Debug Mode)
    debug_logs: List[Dict[str, Any]] = Field(default_factory=list)

    def add_debug_entry(self, component: str, action: str, details: Any):
        """Append runtime observability metadata for developer debug console with deduplication."""
        # Deduplicate consecutive identical actions
        if self.debug_logs:
            last = self.debug_logs[-1]
            if last.get("component") == component and last.get("action") == action:
                last["timestamp"] = time.strftime("%H:%M:%S")
                last["details"] = details
                return

        entry = {
            "timestamp": time.strftime("%H:%M:%S"),
            "component": component,  # "CrewAI", "LangChain", "RAG", "Controller"
            "action": action,
            "details": details
        }
        self.debug_logs.append(entry)

    def add_transcript_turn(self, role: str, message: str, metadata: Optional[Dict[str, Any]] = None):
        """Record dialogue turn in centralized transcript."""
        turn = {
            "timestamp": time.strftime("%H:%M:%S"),
            "role": role,  # "interviewer", "candidate"
            "message": message,
            "metadata": metadata or {}
        }
        self.transcript.append(turn)
