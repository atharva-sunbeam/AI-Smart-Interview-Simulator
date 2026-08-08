import os
import json
import random
import requests
import re
from dotenv import load_dotenv, find_dotenv

# Auto-detect and load .env file from current working directory or workspace root
load_dotenv(find_dotenv(usecwd=True))

from rag_pipeline.rag import RAGPipeline
from agents.knowledge_manager import KnowledgeManager
from agents.role_catalog import get_role_blueprint, get_all_roles

try:
    from crewai import Agent
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False


class LLMManager:
    """
    LLM Engine Client using Groq Cloud API (llama-3.3-70b-versatile) with fallback to Ollama & Smart Offline Mode.
    """
    def __init__(self, provider="auto", model_name="llama-3.3-70b-versatile", api_key=None, host="http://localhost:11434"):
        self.provider = provider
        self.model_name = model_name or "llama-3.3-70b-versatile"
        self.api_key = api_key
        self.host = host
        self.llm = None
        self.is_connected = False
        self._initialize()

    def _initialize(self):
        # Retrieve Groq API Key
        key = self.api_key or os.getenv("GROQ_API_KEY") or os.getenv("GROK_API_KEY")

        if key:
            self.api_key = key
            url = "https://api.groq.com/openai/v1/chat/completions"
            model = self.model_name
            try:
                res = requests.post(
                    url,
                    headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                    json={"model": model, "messages": [{"role": "user", "content": "ping"}], "max_tokens": 5},
                    timeout=5
                )
                if res.status_code == 200:
                    self.is_connected = True
                    self.provider = "groq"
                    self.model_name = model
                    print(f"[LLMManager] Connected to Groq API Engine ({model}) successfully.")
                    return
                else:
                    print(f"[LLMManager] Groq API check status code {res.status_code}: {res.text[:100]}")
            except Exception as e:
                print(f"[LLMManager] Groq API check error: {e}")

        # Fallback to Local Ollama
        try:
            res = requests.get(f"{self.host}/api/tags", timeout=2)
            if res.status_code == 200:
                from langchain_community.chat_models import ChatOllama
                target_model = "mistral"
                self.llm = ChatOllama(model=target_model, base_url=self.host)
                self.is_connected = True
                self.provider = "ollama"
                print(f"[LLMManager] Connected to Ollama local endpoint ({target_model})")
                return
        except Exception:
            pass

        # Smart Offline Fallback Engine
        print("[LLMManager] Operating in Smart Offline Mode.")
        self.is_connected = False
        self.provider = "offline"

    def generate(self, prompt, temperature=0.7):
        if not self.is_connected:
            return None

        if self.provider == "groq" and self.api_key:
            url = "https://api.groq.com/openai/v1/chat/completions"
            model = self.model_name or "llama-3.3-70b-versatile"
            try:
                headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
                payload = {
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": temperature
                }
                res = requests.post(url, headers=headers, json=payload, timeout=15)
                if res.status_code == 200:
                    data = res.json()
                    return data["choices"][0]["message"]["content"].strip()
                else:
                    print(f"[Groq REST API Error] Status {res.status_code}: {res.text[:100]}")
            except Exception as e:
                print(f"[Groq REST API Exception] {e}")

        if self.llm:
            try:
                from langchain_core.messages import HumanMessage
                response = self.llm.invoke([HumanMessage(content=prompt)])
                if hasattr(response, "content"):
                    return response.content.strip()
                return str(response).strip()
            except Exception:
                pass

        return None


class OllamaClient(LLMManager):
    def __init__(self, model="mistral", host="http://localhost:11434"):
        super().__init__(provider="auto", model_name=model, host=host)


class GlobalQuestionRegistry:
    """
    Persistent global registry for previously asked interview questions to guarantee
    cross-session uniqueness.
    """
    def __init__(self, filepath="datasets/processed/global_asked_questions.json"):
        self.filepath = filepath
        self.asked_questions = set()
        self.load()

    def load(self):
        try:
            if os.path.exists(self.filepath):
                with open(self.filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.asked_questions = set(data)
        except Exception as e:
            print(f"[GlobalQuestionRegistry] Load error: {e}")
            self.asked_questions = set()

    def _normalize(self, text):
        if not text:
            return ""
        return re.sub(r'[^\w\s]', '', text.strip().lower())

    def is_asked(self, q_text):
        if not q_text:
            return False
        q_norm = self._normalize(q_text)
        if not q_norm:
            return False

        # 1. Exact string match check
        for past in self.asked_questions:
            past_norm = self._normalize(past)
            if q_norm == past_norm:
                return True

            # 2. Key phrase overlap check (>80% word overlap)
            q_words = set(q_norm.split())
            past_words = set(past_norm.split())
            if len(q_words) > 4 and len(past_words) > 4:
                overlap = len(q_words.intersection(past_words)) / max(len(q_words), len(past_words))
                if overlap > 0.82:
                    return True

        return False

    def add(self, q_text):
        if q_text:
            self.asked_questions.add(q_text.strip())
            self.save()

    def save(self):
        try:
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(list(self.asked_questions), f, indent=2)
        except Exception as e:
            print(f"[GlobalQuestionRegistry] Save error: {e}")


class QuestionGeneratorAgent:
    """
    Strict Difficulty & Blueprint Question Generator Agent supporting Resume Project Deep-Dives.
    """
    def __init__(self, rag_pipeline: RAGPipeline, llm_manager: LLMManager, km: KnowledgeManager = None):
        self.rag = rag_pipeline
        self.llm = llm_manager
        self.km = km or KnowledgeManager()
        self.global_registry = GlobalQuestionRegistry()
        if CREWAI_AVAILABLE:
            self.crew_agent = Agent(
                role="Strict Technical Interview Question Generator",
                goal="Generate non-repeating, strictly difficulty-controlled technical & project-based questions",
                backstory="Lead technical interviewer enforcing strict difficulty tiers and topic progress.",
                verbose=False
            )

    def generate_question(self, role, difficulty, answered_questions, topic=None, skills=None, projects=None, past_history=None):
        """
        Retrieves/Synthesizes a question strictly adhering to `difficulty` (Easy, Medium, Hard),
        blueprint `topic`, candidate `skills`, and candidate project metadata (`projects`).
        Guarantees zero cross-session question repetition.
        """
        all_excluded = set(answered_questions).union(self.global_registry.asked_questions)

        # Handle Project-Based Question Generation
        if topic == "Candidate Resume Project & Real-World Experience" and projects and len(projects) > 0:
            project_data = random.choice(projects)
            if isinstance(project_data, dict):
                proj_name = project_data.get("name", "your project").strip()
                proj_tools_list = project_data.get("tools", [])
                proj_tools = ", ".join(proj_tools_list) if proj_tools_list else "the technologies involved"
                proj_desc = project_data.get("description", proj_name).strip()
            else:
                proj_name = str(project_data)[:50].strip()
                proj_tools = "the technologies involved"
                proj_desc = proj_name

            if difficulty == "Easy":
                q_text = f"In your project '{proj_name}' ({proj_desc[:60]}), what specific tools and technologies did you use (such as {proj_tools}), and why did you choose them?"
                exp_ans = f"Explanation of tool selection ({proj_tools}) for project '{proj_name}' and candidate's core role."
            elif difficulty == "Medium":
                q_text = f"In your project '{proj_name}' ({proj_desc[:60]}), what key technical implementation or integration challenges did you encounter while working with {proj_tools}, and how did you resolve them?"
                exp_ans = f"Detailed breakdown of implementation challenges with {proj_tools} in '{proj_name}' and debugging steps."
            else:  # Hard
                q_text = f"How would you re-architect or optimize your project '{proj_name}' ({proj_desc[:60]}), built with {proj_tools}, to handle high concurrency, 100x scale, and zero-downtime failover?"
                exp_ans = f"Advanced system architecture strategies for scaling '{proj_name}' and {proj_tools} including caching and load balancing."

            if self.llm.is_connected:
                easy_prompt_instruction = f"Formulate a question asking strictly: In your project '{proj_name}' ({proj_desc}), what specific tools and technologies did you use (such as {proj_tools}), and why did you choose them?"
                medium_prompt_instruction = f"Formulate a question asking strictly: In your project '{proj_name}' ({proj_desc}), what key technical implementation or integration challenges did you encounter while using {proj_tools}, and how did you solve them?"
                hard_prompt_instruction = f"Formulate a question asking strictly: How would you re-architect or optimize '{proj_name}' ({proj_desc}), built using {proj_tools}, for 100x scale, high concurrency, and distributed failover?"

                selected_instruction = easy_prompt_instruction if difficulty == "Easy" else (medium_prompt_instruction if difficulty == "Medium" else hard_prompt_instruction)

                recent_past = list(self.global_registry.asked_questions)[-10:]
                past_str = "\n- ".join(recent_past) if recent_past else "None"

                prompt = (
                    f"You are a technical interviewer evaluating a candidate for {role} (Difficulty Level: STRICTLY {difficulty}).\n"
                    f"Project Name: {proj_name}\n"
                    f"Project Summary: {proj_desc}\n"
                    f"Technologies / Tools Used: {proj_tools}\n"
                    f"{selected_instruction}\n"
                    f"CRITICAL: DO NOT repeat any past questions:\n- {past_str}\n\n"
                    f"Format output strictly as a JSON object:\n"
                    f'{{\n  "question": "<your project question>",\n  "expected_answer": "<key expected points>"\n}}'
                )
                response = self.llm.generate(prompt)
                if response:
                    try:
                        clean_res = re.sub(r'```json\s*|\s*```', '', response).strip()
                        parsed = json.loads(clean_res)
                        if "question" in parsed and "expected_answer" in parsed:
                            new_q = parsed["question"]
                            if not self.global_registry.is_asked(new_q):
                                self.global_registry.add(new_q)
                                return {
                                    "question": new_q,
                                    "raw_question": new_q,
                                    "expected_answer": parsed["expected_answer"],
                                    "topic": "Candidate Resume Project & Real-World Experience",
                                    "difficulty": difficulty
                                }
                    except Exception:
                        pass

            self.global_registry.add(q_text)
            return {
                "question": q_text,
                "raw_question": q_text,
                "expected_answer": exp_ans,
                "topic": "Candidate Resume Project & Real-World Experience",
                "difficulty": difficulty
            }

        # Step 1: Attempt retrieval from KnowledgeManager JSON pools
        km_candidates = self.km.get_questions_for_role(
            role=role,
            difficulty=difficulty,
            topic=topic,
            excluded_questions=all_excluded
        )

        selected = None
        if km_candidates:
            selected = random.choice(km_candidates)
        else:
            # Fallback 1: Try without topic constraint in JSON pools
            km_candidates_no_topic = self.km.get_questions_for_role(
                role=role,
                difficulty=difficulty,
                excluded_questions=all_excluded
            )
            if km_candidates_no_topic:
                selected = random.choice(km_candidates_no_topic)

        # Step 2: If no JSON match, fallback to ChromaDB RAG Search
        if not selected:
            query_str = f"{topic} {skills[0]}" if (skills and topic) else (topic or role)
            retrieved = self.rag.retrieve_questions(role=role, difficulty=difficulty, query=query_str, k=25)
            available = [r for r in retrieved if not self.global_registry.is_asked(r["question"])]
            if available:
                selected = random.choice(available)

        # Emergency Fallback
        if not selected:
            selected = {
                "question": f"Explain the core principles and practical usage of {topic or 'key software concepts'} in {role}.",
                "answer": f"Core principles of {topic or 'software engineering'} focus on modularity, correct syntax, and robust error handling.",
                "topic": topic or "General",
                "difficulty": difficulty
            }

        # Contextual history snippet from past answered questions
        history_context = ""
        if past_history and len(past_history) > 0:
            last_item = past_history[-1]
            history_context = f"\nPrevious Candidate Answer Score: {last_item.get('score', 5.0)}/10. (Feedback: {last_item.get('feedback', '')[:100]})\n"

        # Step 3: LLM Synthesis with STRICT DIFFICULTY RULE PROMPTS & ZERO REPETITION
        if self.llm.is_connected:
            difficulty_rules = {
                "Easy": "STRICT RULE EASY: Ask ONLY beginner concepts, definitions, basic syntax, or simple usage. DO NOT ask advanced system design, distributed systems, or complex optimization.",
                "Medium": "STRICT RULE MEDIUM: Ask intermediate implementation, real-world usage, practical coding scenarios, or moderate debugging. DO NOT ask basic definitions or extreme architecture design.",
                "Hard": "STRICT RULE HARD: Ask advanced concepts, system architecture, performance optimization, concurrency, or distributed systems. DO NOT ask simple syntax definitions."
            }
            rule_str = difficulty_rules.get(difficulty, difficulty_rules["Medium"])

            recent_past = list(self.global_registry.asked_questions)[-12:]
            past_str = "\n- ".join(recent_past) if recent_past else "None"

            prompt = (
                f"You are a strict technical interviewer evaluating a candidate for the position of {role}.\n"
                f"Active Topic: {topic or selected.get('topic', 'Core Concept')}\n"
                f"Selected Difficulty: {difficulty} (MUST REMAIN STRICTLY {difficulty})\n"
                f"{rule_str}\n"
                f"{history_context}\n"
                f"Reference Concept: {selected['question']}\n\n"
                f"Task: Generate a crisp, unique technical question tailored specifically for {role}.\n"
                f"CRITICAL RULES:\n"
                f"1. DO NOT repeat or duplicate any of these past questions across any sessions:\n- {past_str}\n"
                f"2. Enforce the difficulty constraint strictly ({difficulty}).\n"
                f"3. Keep question length between 15 and 30 words.\n\n"
                f"Format output strictly as a JSON object:\n"
                f'{{\n  "question": "<your unique new question>",\n  "expected_answer": "<key points expected in answer>"\n}}'
            )

            response = self.llm.generate(prompt)
            if response:
                try:
                    clean_res = re.sub(r'```json\s*|\s*```', '', response).strip()
                    parsed = json.loads(clean_res)
                    if "question" in parsed and "expected_answer" in parsed:
                        new_q = parsed["question"]
                        if not self.global_registry.is_asked(new_q):
                            self.global_registry.add(new_q)
                            self.global_registry.add(selected["question"])
                            return {
                                "question": new_q,
                                "raw_question": selected["question"],
                                "expected_answer": parsed["expected_answer"],
                                "topic": topic or selected.get("topic", "General"),
                                "difficulty": difficulty
                            }
                except Exception:
                    pass

        self.global_registry.add(selected["question"])
        return {
            "question": selected["question"],
            "raw_question": selected["question"],
            "expected_answer": selected["answer"],
            "topic": topic or selected.get("topic", "General"),
            "difficulty": difficulty
        }


class AnswerEvaluatorAgent:
    def __init__(self, llm_manager: LLMManager):
        self.llm = llm_manager
        if CREWAI_AVAILABLE:
            self.crew_agent = Agent(
                role="Technical Answer Evaluator",
                goal="Assess technical answer accuracy, depth, and missing keywords objectively",
                backstory="Senior engineering manager evaluating conceptual clarity and practical correctness.",
                verbose=False
            )

    def evaluate_answer(self, question, expected_answer, user_answer):
        """Evaluates standalone question-answer response objectively."""
        if not user_answer or len(user_answer.strip()) < 5:
            return {
                "score": 1.0,
                "feedback": "No answer was provided, or the answer was too short to evaluate. Please try explaining key terms and concepts."
            }

        if self.llm.is_connected:
            prompt = (
                f"You are a supportive technical interviewer evaluating a candidate's response.\n\n"
                f"Question Asked: {question}\n"
                f"Expected Key Points: {expected_answer}\n"
                f"Candidate's Answer: {user_answer}\n\n"
                f"Respond strictly in this format:\n"
                f"Score: <integer from 1 to 10>\n"
                f"Feedback: <2-3 sentence constructive feedback highlighting correct points and helpful guidance>"
            )
            response = self.llm.generate(prompt)
            if response:
                score_match = re.search(r'Score:\s*(\d+)', response, re.IGNORECASE)
                feedback_match = re.search(r'Feedback:\s*(.*)', response, re.IGNORECASE | re.DOTALL)

                score = float(score_match.group(1)) if score_match else 5.0
                feedback = feedback_match.group(1).strip() if feedback_match else response
                return {
                    "score": min(max(score, 1.0), 10.0),
                    "feedback": feedback
                }

        # Offline Keyword Fallback
        expected_words = set(re.findall(r'\b\w{4,}\b', expected_answer.lower()))
        user_words = set(re.findall(r'\b\w{4,}\b', user_answer.lower()))

        stopwords = {"with", "that", "this", "they", "them", "from", "their", "will", "would", "about", "there", "these", "which", "could", "should"}
        expected_keywords = expected_words - stopwords

        matched_keywords = expected_keywords.intersection(user_words)
        overlap_ratio = len(matched_keywords) / len(expected_keywords) if expected_keywords else 0.0

        words_count = len(user_answer.split())
        length_factor = min(words_count / 40.0, 1.0)

        score = 1.0 + (overlap_ratio * 7.0) + (length_factor * 2.0)
        score = round(min(max(score, 1.0), 10.0), 1)

        unmatched = list(expected_keywords - user_words)[:4]
        matched = list(matched_keywords)[:4]

        feedback = "Your answer is on the right track! "
        if score >= 8.0:
            feedback += f"Excellent explanation. You correctly covered key aspects like: {', '.join(matched)}. "
        elif score >= 5.0:
            feedback += f"Good start. You mentioned important points like {', '.join(matched)}, but missed explaining related details: {', '.join(unmatched)}. "
        else:
            feedback += f"The explanation was incomplete. To improve, make sure to mention and define terms like: {', '.join(unmatched)}. "

        return {
            "score": score,
            "feedback": feedback
        }


class FollowUpAgent:
    def __init__(self, llm_manager: LLMManager):
        self.llm = llm_manager
        if CREWAI_AVAILABLE:
            self.crew_agent = Agent(
                role="Probing Follow-up Interviewer",
                goal="Generate encouraging follow-up questions matching difficulty tier",
                backstory="Specialist in probing candidate depth and practical use cases.",
                verbose=False
            )

    def generate_followup(self, question, expected_answer, user_answer, role="Engineering Candidate", difficulty="Medium"):
        if self.llm.is_connected:
            prompt = (
                f"You are a technical interviewer for {role} (Difficulty: {difficulty}).\n"
                f"Main Question: {question}\n"
                f"Candidate's Answer: {user_answer}\n\n"
                f"Task: Generate one encouraging follow-up question (15 to 25 words) matching difficulty level {difficulty}.\n"
                f"Keep it relevant to the candidate's answer."
            )
            followup = self.llm.generate(prompt)
            if followup:
                return followup.strip()

        return f"Could you elaborate on how you would apply this concept in a real-world project for {role}?"


class FeedbackAgent:
    def __init__(self, llm_manager: LLMManager):
        self.llm = llm_manager
        if CREWAI_AVAILABLE:
            self.crew_agent = Agent(
                role="Executive Performance Reporter",
                goal="Compile comprehensive technical feedback reports and statistics",
                backstory="Lead interviewer responsible for candidate hiring recommendations and skill gap analysis.",
                verbose=False
            )

    def generate_report(self, role, history):
        total_questions = len(history)
        if total_questions == 0:
            return "No interview history recorded."

        average_score = sum(item["score"] for item in history) / total_questions
        average_score = round(average_score, 1)

        topic_scores = {}
        for item in history:
            topic = item.get("topic", "General")
            if topic not in topic_scores:
                topic_scores[topic] = []
            topic_scores[topic].append(item["score"])

        topic_perf = {}
        for topic, scores in topic_scores.items():
            topic_perf[topic] = round(sum(scores) / len(scores), 1)

        if self.llm.is_connected:
            history_str = ""
            for i, h in enumerate(history):
                q_type = "Follow-up" if h.get("is_followup") else "Main Q"
                history_str += f"Q{i+1} ({q_type}): {h['question']}\nCandidate Answer: {h['answer']}\nScore: {h['score']}/10\nFeedback: {h['feedback']}\n\n"

            prompt = (
                f"Generate a professional, structured interview feedback report for a candidate who interviewed for the {role} position.\n\n"
                f"Summary Stats:\n"
                f"- Questions Evaluated: {total_questions}\n"
                f"- Average Score: {average_score}/10\n\n"
                f"Detail Logs:\n"
                f"{history_str}\n"
                f"Please format your response strictly in markdown with the following exact layout:\n"
                f"# Technical Interview Evaluation Report\n\n"
                f"## Executive Summary\n<executive summary text>\n\n"
                f"## Topic-wise Breakdown\n"
                f"YOU MUST FORMAT THIS SECTION AS A MARKDOWN TABLE with columns:\n"
                f"| Domain / Sub-Topic | Average Score | Evaluation |\n"
                f"|---|---|---|\n"
                f"| <topic> | <score>/10 | <Proficient/Needs Work> |\n\n"
                f"## Key Strengths\n<bullet points>\n\n"
                f"## Areas for Improvement\n<bullet points>\n\n"
                f"## Overall Recommendation\n<final recommendation>"
            )
            report = self.llm.generate(prompt)
            if report:
                return report

        report = f"# Technical Interview Evaluation Report\n\n"
        report += f"## Executive Summary\n"
        report += f"The candidate underwent a structured technical interview simulating the **{role}** profile.\n"
        report += f"- **Total Questions Evaluated**: {total_questions}\n"
        report += f"- **Overall Technical Score**: **{average_score} / 10**\n"

        status = "Strong Hire" if average_score >= 8.0 else ("Hire" if average_score >= 6.0 else "Needs Improvement / No Hire")
        report += f"- **Interview Status Recommendation**: **{status}**\n\n"

        report += f"## Topic-wise Breakdown\n"
        report += "Below is the candidate's average scoring performance across technical sub-domains:\n\n"
        report += "| Domain / Sub-Topic | Average Score | Evaluation |\n"
        report += "|---|---|---|\n"
        for topic, score in topic_perf.items():
            rating = "Excellent" if score >= 8.0 else ("Proficient" if score >= 6.0 else "Developing")
            report += f"| {topic} | {score} / 10 | {rating} |\n"
        report += "\n"

        report += f"## Key Strengths\n"
        strengths = [t for t, s in topic_perf.items() if s >= 6.0]
        if strengths:
            for s in strengths:
                report += f"- **{s}**: Demonstrated solid conceptual understanding during evaluation.\n"
        else:
            report += "- The candidate showed a basic grasp of introductory concepts but needs to work on detailing explanations.\n"
        report += "\n"

        report += f"## Areas for Improvement\n"
        weaknesses = [t for t, s in topic_perf.items() if s < 6.0]
        if weaknesses:
            for w in weaknesses:
                report += f"- **{w}**: Candidate missed key technical elements. Focus on refining syntax and core concepts in this topic.\n"
        else:
            report += "- No major conceptual gaps were identified. Focus on production-scale system design details to reach the next tier.\n"
        report += "\n"

        report += f"## Overall Recommendation\n"
        if average_score >= 8.0:
            report += "The candidate exhibits high technical proficiency and is strongly recommended."
        elif average_score >= 6.0:
            report += "The candidate has a solid foundation for standard engineering roles."
        else:
            report += "The candidate requires further preparation in foundational principles."

        return report


class SuperAgent:
    """
    Supervising Orchestrator Agent with Interview Blueprinting & Strict Difficulty Enforcement.
    """
    def __init__(self, rag_pipeline: RAGPipeline, llm_manager: LLMManager = None):
        self.llm_manager = llm_manager or LLMManager()
        self.rag = rag_pipeline
        self.km = KnowledgeManager()
        self.qgen_agent = QuestionGeneratorAgent(self.rag, self.llm_manager, self.km)
        self.eval_agent = AnswerEvaluatorAgent(self.llm_manager)
        self.followup_agent = FollowUpAgent(self.llm_manager)
        self.feedback_agent = FeedbackAgent(self.llm_manager)

    def create_interview_blueprint(self, role, skills=None, projects=None, count=5):
        """
        Creates an ordered interview blueprint for the role, re-ordering topics based on skills
        and injecting Project-Based Question slots when count > 5 according to the defined ratio.
        """
        raw_blueprint = get_role_blueprint(role)

        if skills:
            skills_flat = [s.lower() for s in skills]
            prioritized = []
            remaining = []
            for topic in raw_blueprint:
                topic_lower = topic.lower()
                if any(s in topic_lower or topic_lower in s for s in skills_flat):
                    prioritized.append(topic)
                else:
                    remaining.append(topic)
            blueprint = prioritized + remaining
        else:
            blueprint = list(raw_blueprint)

        # Inject Project-Based Question slots when count > 5 and projects exist
        if count > 5 and projects and len(projects) > 0:
            num_project_q = 1 if count <= 7 else 2
            project_topic = "Candidate Resume Project & Real-World Experience"

            if num_project_q >= 1 and len(blueprint) >= 3:
                blueprint.insert(3, project_topic)
            if num_project_q >= 2 and len(blueprint) >= 6:
                blueprint.insert(6, project_topic)

        return blueprint

    def get_questions(self, role, difficulty, count, skills=None, projects=None):
        answered = set()
        questions = []
        blueprint = self.create_interview_blueprint(role, skills, projects, count)

        for i in range(count):
            topic = blueprint[i % len(blueprint)]
            q_data = self.qgen_agent.generate_question(
                role=role,
                difficulty=difficulty,
                answered_questions=answered,
                topic=topic,
                skills=skills,
                projects=projects
            )
            if q_data:
                questions.append(q_data)
                answered.add(q_data["raw_question"])
        return questions

    def get_adaptive_difficulty(self, current_difficulty, history, adaptive_mode=False):
        """
        Difficulty Control: If `adaptive_mode` is False (default), strictly LOCKS the difficulty
        to `current_difficulty`.
        """
        if not adaptive_mode:
            return current_difficulty

        if not history:
            return current_difficulty

        recent_scores = [h["score"] for h in history[-2:]]
        avg_score = sum(recent_scores) / len(recent_scores)

        levels = ["Easy", "Medium", "Hard"]
        current_idx = levels.index(current_difficulty) if current_difficulty in levels else 1

        if avg_score >= 8.0 and current_idx < 2:
            return levels[current_idx + 1]
        elif avg_score < 5.0 and current_idx > 0:
            return levels[current_idx - 1]
        return current_difficulty

    def evaluate(self, question, expected_answer, user_answer):
        return self.eval_agent.evaluate_answer(question, expected_answer, user_answer)

    def generate_followup(self, question, expected_answer, user_answer, role="Engineering Candidate", difficulty="Medium"):
        return self.followup_agent.generate_followup(question, expected_answer, user_answer, role=role, difficulty=difficulty)

    def generate_report(self, role, history):
        self.save_session_learning(role, history)
        return self.feedback_agent.generate_report(role, history)

    def save_session_learning(self, role, history):
        try:
            store_dir = "datasets/processed"
            os.makedirs(store_dir, exist_ok=True)
            memory_file = os.path.join(store_dir, "learning_memory.json")

            existing_memory = []
            if os.path.exists(memory_file):
                with open(memory_file, "r", encoding="utf-8") as f:
                    try:
                        existing_memory = json.load(f)
                    except Exception:
                        existing_memory = []

            new_entries = []
            for item in history:
                entry = {
                    "role": role,
                    "topic": item.get("topic", "General"),
                    "question": item.get("question"),
                    "answer": item.get("answer"),
                    "score": item.get("score"),
                    "feedback": item.get("feedback")
                }
                new_entries.append(entry)

            existing_memory.extend(new_entries)
            with open(memory_file, "w", encoding="utf-8") as f:
                json.dump(existing_memory, f, indent=2)

            high_quality = [item for item in history if item.get("score", 0) >= 7.0]
            if high_quality:
                self.rag.add_session_to_knowledge_base(role, high_quality)
                print(f"[SuperAgent Self-Learning] Enriched RAG Vector Store with {len(high_quality)} new Q&A pairs.")

        except Exception as e:
            print(f"[SuperAgent Self-Learning Error] {e}")
