from typing import List, Optional
from pydantic import BaseModel, Field


class AnswerEvaluation(BaseModel):
    """Expanded structured evaluation output for candidate responses."""
    technical_score: float = Field(..., description="Score from 0.0 to 10.0 for technical accuracy")
    relevance_score: float = Field(..., description="Score from 0.0 to 10.0 for relevance to the question asked")
    completeness_score: float = Field(..., description="Score from 0.0 to 10.0 for covering key expected concepts")
    clarity_score: float = Field(..., description="Score from 0.0 to 10.0 for clarity of explanation")
    depth_score: float = Field(..., description="Score from 0.0 to 10.0 for depth of technical understanding")
    overall_score: float = Field(..., description="Weighted overall score calculated from sub-scores (0.0 to 10.0)")
    
    strengths: List[str] = Field(default_factory=list, description="Key correct points and technical insights mentioned")
    weaknesses: List[str] = Field(default_factory=list, description="Areas where candidate explanation fell short")
    missing_concepts: List[str] = Field(default_factory=list, description="Essential technical concepts or keywords missed")
    incorrect_points: List[str] = Field(default_factory=list, description="Technical misconceptions or inaccuracies identified")
    
    feedback: str = Field(..., description="Detailed, actionable technical feedback teaching the candidate")
    recommended_follow_up: Optional[str] = Field(default=None, description="Targeted follow-up question if probing is needed")
    follow_up_needed: bool = Field(default=False, description="Whether a targeted follow-up question is recommended")


class InterviewDecision(BaseModel):
    """Structured decision output for interview progression."""
    action: str = Field(..., description="Next action: 'ask_next', 'ask_followup', or 'end_interview'")
    next_question: str = Field(..., description="The exact question text to be asked to the candidate")
    expected_answer: str = Field(..., description="Key expected points in the answer")
    topic: str = Field(..., description="Technical topic area for the question")
    difficulty: str = Field(..., description="Difficulty level: 'Easy', 'Medium', or 'Hard'")
    reasoning_summary: str = Field(..., description="Brief rationale for this decision")
