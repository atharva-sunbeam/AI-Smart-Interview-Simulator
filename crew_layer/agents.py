from crewai import Agent
from core.llm_factory import LLMFactory


def create_interview_crew_agents(llm_factory: LLMFactory = None):
    """
    Constructs and returns the 4 specialized CrewAI Agents for multi-agent interview orchestration.
    """
    factory = llm_factory or LLMFactory()
    crew_llm = factory.get_crewai_llm()

    supervisor = Agent(
        role="Interview Supervisor Agent",
        goal="Oversee the high-level technical interview workflow, ensure interview policy adherence, and dictate phase transitions.",
        backstory="""You are the Engineering Director and Head of Technical Recruiting. 
        You supervise the interview session, coordinate the question strategist and answer evaluator, 
        and decide when to adapt difficulty or conclude the interview.""",
        llm=crew_llm,
        verbose=True,
        allow_delegation=False
    )

    question_strategist = Agent(
        role="Question Strategy Agent",
        goal="Select precise blueprint topics, enforce strict difficulty tiers, integrate resume project deep-dives, and adapt questioning to missing candidate concepts.",
        backstory="""You are a Lead Staff Architect skilled in technical assessment design. 
        You craft non-repetitive, challenging questions tailored to the candidate's exact role and past answer strengths/weaknesses.""",
        llm=crew_llm,
        verbose=True,
        allow_delegation=False
    )

    interviewer = Agent(
        role="Conversational Interviewer Agent",
        goal="Formulate natural, professional, encouraging human interviewer phrasing for questions and follow-ups.",
        backstory="""You are a Senior Principal Engineer conducting a live technical interview. 
        You speak warmly, professionally, and conversationally, acknowledging candidate answers naturally before asking the next question.""",
        llm=crew_llm,
        verbose=True,
        allow_delegation=False
    )

    evaluator = Agent(
        role="Technical Answer Evaluator Agent",
        goal="Assess candidate answers objectively, identifying exact technical scores, missing concepts, and key strengths.",
        backstory="""You are a strict Technical Assessment Specialist. You evaluate technical accuracy, relevance, and depth without bias, 
        highlighting specific conceptual gaps for adaptive probing.""",
        llm=crew_llm,
        verbose=True,
        allow_delegation=False
    )

    return {
        "supervisor": supervisor,
        "strategist": question_strategist,
        "interviewer": interviewer,
        "evaluator": evaluator
    }
