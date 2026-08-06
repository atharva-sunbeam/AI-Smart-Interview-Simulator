import os
import json
import random
import requests
import re
from dotenv import load_dotenv, find_dotenv

# Auto-detect and load .env file from current working directory or workspace root
load_dotenv(find_dotenv(usecwd=True))

from rag_pipeline.rag import RAGPipeline

try:
    from crewai import Agent
    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False

class LLMManager:
    """
    Unified Multi-Tier LLM Client with auto-detection for Grok (xAI), Groq (gsk_), OpenAI (sk-), and Ollama.
    """
    def __init__(self, provider="auto", model_name=None, api_key=None, host="http://localhost:11434"):
        self.provider = provider
        self.model_name = model_name
        self.api_key = api_key
        self.host = host
        self.llm = None
        self.is_connected = False
        self._initialize()

    def _initialize(self):
        key = self.api_key or os.getenv("GROK_API_KEY") or os.getenv("GROQ_API_KEY") or os.getenv("XAI_API_KEY") or os.getenv("OPENAI_API_KEY")

        if key:
            self.api_key = key
            # 1. Groq Cloud API (keys starting with gsk_)
            if key.startswith("gsk_"):
                url = "https://api.groq.com/openai/v1/chat/completions"
                model = self.model_name or "llama-3.3-70b-versatile"
                try:
                    res = requests.post(
                        url,
                        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                        json={"model": model, "messages": [{"role": "user", "content": "ping"}], "max_tokens": 5},
                        timeout=5
                    )
                    if res.status_code == 200:
                        self.is_connected = True
                        self.provider = "grok"
                        self.model_name = model
                        print(f"[LLMManager] Connected to Groq API Engine ({model}) successfully.")
                        return
                except Exception as e:
                    print(f"[LLMManager] Groq API check error: {e}")

            # 2. xAI Grok API (keys starting with xai-)
            elif key.startswith("xai-"):
                url = "https://api.x.ai/v1/chat/completions"
                model = self.model_name or "grok-2"
                try:
                    res = requests.post(
                        url,
                        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                        json={"model": model, "messages": [{"role": "user", "content": "ping"}], "max_tokens": 5},
                        timeout=5
                    )
                    if res.status_code == 200:
                        self.is_connected = True
                        self.provider = "grok"
                        self.model_name = model
                        print(f"[LLMManager] Connected to xAI Grok API ({model}) successfully.")
                        return
                except Exception as e:
                    print(f"[LLMManager] xAI API check error: {e}")

            # 3. Standard OpenAI format API
            else:
                url = "https://api.openai.com/v1/chat/completions"
                model = self.model_name or "gpt-4o-mini"
                try:
                    res = requests.post(
                        url,
                        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                        json={"model": model, "messages": [{"role": "user", "content": "ping"}], "max_tokens": 5},
                        timeout=5
                    )
                    if res.status_code == 200:
                        self.is_connected = True
                        self.provider = "grok"
                        self.model_name = model
                        print(f"[LLMManager] Connected to OpenAI API ({model}).")
                        return
                except Exception:
                    pass

        # 4. Fallback to Local Ollama
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

        # 5. Smart Offline Fallback Engine
        print("[LLMManager] Operating in Smart Offline Mode.")
        self.is_connected = False
        self.provider = "offline"

    def generate(self, prompt, temperature=0.7):
        if not self.is_connected:
            return None

        if self.provider == "grok" and self.api_key:
            if self.api_key.startswith("gsk_"):
                url = "https://api.groq.com/openai/v1/chat/completions"
                model = self.model_name or "llama-3.3-70b-versatile"
            elif self.api_key.startswith("xai-"):
                url = "https://api.x.ai/v1/chat/completions"
                model = self.model_name or "grok-2"
            else:
                url = "https://api.openai.com/v1/chat/completions"
                model = self.model_name or "gpt-4o-mini"

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
                    print(f"[LLM REST API Error] Status {res.status_code}: {res.text[:100]}")
            except Exception as e:
                print(f"[LLM REST API Exception] {e}")

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

FALLBACK_FOLLOWUPS = [
    ({"docker", "container"}, "What is the purpose of Docker container isolation, and how do you check running container logs?"),
    ({"kubernetes", "k8s", "pod"}, "What is a Pod in Kubernetes, and what command do you use to view pod status?"),
    ({"terraform", "iac"}, "What is Terraform state, and why is Infrastructure as Code useful in software projects?"),
    ({"ci/cd", "jenkins", "github actions"}, "What are the main stages of a CI/CD pipeline, and why do we automate testing?"),
    ({"rag", "vector", "embedding", "chromadb"}, "What is the purpose of vector embeddings in RAG, and why do we retrieve relevant documents?"),
    ({"llm", "langchain", "crewai"}, "What is LangChain used for, and how do agents execute tasks using tools?"),
    ({"spark", "pyspark"}, "What is Apache Spark used for, and how does it process large datasets in memory?"),
    ({"kafka"}, "What is Apache Kafka used for in distributed applications?"),
    ({"decorator"}, "What is a Python decorator, and how do you apply it to a function?"),
    ({"tuple", "list"}, "What is the main difference between a list and a tuple in Python?")
]

class QuestionGeneratorAgent:
    def __init__(self, rag_pipeline: RAGPipeline, llm_manager: LLMManager):
        self.rag = rag_pipeline
        self.llm = llm_manager
        if CREWAI_AVAILABLE:
            self.crew_agent = Agent(
                role="Technical Interviewer for Entry-Level Engineering Candidates",
                goal="Synthesize clear, accessible, entry-level technical interview questions using ChromaDB RAG concepts",
                backstory="Friendly technical interviewer evaluating core foundational knowledge and practical skills for freshers.",
                verbose=False
            )

    def generate_question(self, role, difficulty, answered_questions, skills=None):
        query_str = " ".join(skills) if skills else "core concepts"
        
        retrieved = self.rag.retrieve_questions(role=role, difficulty=difficulty, query=query_str, k=10)
        available = [r for r in retrieved if r["question"] not in answered_questions]
        
        if not available:
            fallback_retrieved = self.rag.retrieve_questions(role=role, difficulty=difficulty, k=15)
            available = [r for r in fallback_retrieved if r["question"] not in answered_questions]

        if not available:
            fallback_retrieved = self.rag.retrieve_questions(role=role, k=20)
            available = [r for r in fallback_retrieved if r["question"] not in answered_questions]

        if not available:
            fallback_retrieved = self.rag.retrieve_questions(role=None, difficulty=difficulty, query=query_str, k=15)
            available = [r for r in fallback_retrieved if r["question"] not in answered_questions]

        if not available:
            fallback_retrieved = self.rag.retrieve_questions(role=None, query=query_str, k=20)
            available = [r for r in fallback_retrieved if r["question"] not in answered_questions]

        if not available:
            return None

        selected = available[0]

        # Fresher-oriented LLM Question Synthesis (70-80% clear foundational, 20-30% practical application)
        if self.llm.is_connected:
            question_styles = [
                "clear conceptual question explaining the core concept and its purpose (15 to 25 words)",
                "practical foundational question on how to use this concept in a project (20 to 30 words)",
                "clear conceptual question explaining why we use this concept (15 to 25 words)",
                "simple practical scenario question for a fresher (20 to 30 words)"
            ]
            chosen_style = random.choice(question_styles)

            prompt = (
                f"You are a friendly technical interviewer interviewing an Entry-Level Candidate / Fresher for the position of {role} (Stage: {difficulty}).\n"
                f"Target Audience: Recent Graduates / Freshers with foundational computer science & engineering knowledge.\n"
                f"RAG Background Topic: {selected['topic']}\n"
                f"Reference Concept: {selected['question']}\n\n"
                f"Task: Synthesize a clear, beginner-friendly, practical technical question in real time tailored specifically for a fresher applying for {role}.\n"
                f"CRITICAL RULES:\n"
                f"1. DO NOT ask heavy senior-level system design or 'Design an architecture...' questions.\n"
                f"2. Keep the question clear, practical, and accessible (Style: {chosen_style}).\n"
                f"3. Keep the question length STRICTLY between 15 and 30 words. Simple and direct.\n\n"
                f"Format output strictly as a JSON object:\n"
                f'{{\n  "question": "<your new question>",\n  "expected_answer": "<key basic points expected in answer>"\n}}'
            )
            response = self.llm.generate(prompt)
            if response:
                try:
                    clean_res = re.sub(r'```json\s*|\s*```', '', response).strip()
                    parsed = json.loads(clean_res)
                    if "question" in parsed and "expected_answer" in parsed:
                        return {
                            "question": parsed["question"],
                            "raw_question": selected["question"],
                            "expected_answer": parsed["expected_answer"],
                            "topic": selected["topic"],
                            "difficulty": difficulty
                        }
                except Exception:
                    pass

        return {
            "question": selected["question"],
            "raw_question": selected["question"],
            "expected_answer": selected["answer"],
            "topic": selected["topic"],
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
        if not user_answer or len(user_answer.strip()) < 5:
            return {
                "score": 1.0,
                "feedback": "No answer was provided, or the answer was too short to evaluate. Please try explaining key terms and concepts."
            }

        if self.llm.is_connected:
            prompt = (
                f"You are a supportive technical interviewer evaluating a fresher's response.\n\n"
                f"Question: {question}\n"
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
                goal="Generate friendly, entry-level follow-up questions for partially answered concepts",
                backstory="Specialist in helping freshers elaborate on technical concepts and practical applications.",
                verbose=False
            )

    def generate_followup(self, question, expected_answer, user_answer, role="Engineering Candidate"):
        """
        Generates a friendly, entry-level follow-up question (15-25 words) in real time.
        """
        if self.llm.is_connected:
            prompt = (
                f"You are a friendly technical interviewer for an entry-level / fresher candidate applying for {role}.\n"
                f"Main Question Asked: {question}\n"
                f"Candidate's Answer: {user_answer}\n\n"
                f"Task: Generate one short, encouraging follow-up question (15 to 25 words) suitable for a fresher to help them explain a specific detail or practical use case.\n"
                f"Do NOT ask complex senior system design questions. Keep it simple and approachable."
            )
            followup = self.llm.generate(prompt)
            if followup:
                return followup.strip()

        # Scoped phrase-matching fallback
        text = (question + " " + user_answer).lower()
        for kw_set, followup_q in FALLBACK_FOLLOWUPS:
            if any(kw in text for kw in kw_set):
                return followup_q
                
        return f"Could you briefly explain how you would use this concept in a project for a {role}?"


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
            topic = item["topic"]
            if topic not in topic_scores:
                topic_scores[topic] = []
            topic_scores[topic].append(item["score"])

        topic_perf = {}
        for topic, scores in topic_scores.items():
            topic_perf[topic] = round(sum(scores) / len(scores), 1)

        if self.llm.is_connected:
            history_str = ""
            for i, h in enumerate(history):
                history_str += f"Q{i+1}: {h['question']}\nCandidate Answer: {h['answer']}\nScore: {h['score']}/10\nFeedback: {h['feedback']}\n\n"
            
            prompt = (
                f"Generate a professional, structured interview feedback report for a candidate who interviewed for the {role} position.\n\n"
                f"Summary Stats:\n"
                f"- Questions Asked: {total_questions}\n"
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
                report += f"- **{s}**: Demonstrated solid conceptual understanding and successfully recalled essential keywords during verification.\n"
        else:
            report += "- The candidate showed a basic grasp of introductory concepts but needs to work on detailing core explanations.\n"
        report += "\n"

        report += f"## Areas for Improvement\n"
        weaknesses = [t for t, s in topic_perf.items() if s < 6.0]
        if weaknesses:
            for w in weaknesses:
                report += f"- **{w}**: Candidate missed key technical elements during question-answer verification. Focus on deep-diving into syntax and architectural details of this topic.\n"
        else:
            report += "- No major conceptual gaps were identified. To reach the next tier, focus on refining production-scale system design details.\n"
        report += "\n"

        report += f"## Overall Recommendation\n"
        if average_score >= 8.0:
            report += "The candidate exhibits excellent technical proficiency and is highly recommended for advanced engineering roles."
        elif average_score >= 6.0:
            report += "The candidate has a solid foundation and can handle standard engineering tasks."
        else:
            report += "The candidate requires further preparation in foundational principles."

        return report


class SuperAgent:
    """
    Supervising Orchestrator Agent with Adaptive Stage Progression & System Self-Learning.
    """
    def __init__(self, rag_pipeline: RAGPipeline, llm_manager: LLMManager = None):
        self.llm_manager = llm_manager or LLMManager()
        self.rag = rag_pipeline
        self.qgen_agent = QuestionGeneratorAgent(self.rag, self.llm_manager)
        self.eval_agent = AnswerEvaluatorAgent(self.llm_manager)
        self.followup_agent = FollowUpAgent(self.llm_manager)
        self.feedback_agent = FeedbackAgent(self.llm_manager)

    def get_questions(self, role, difficulty, count, skills=None):
        answered = set()
        questions = []
        for _ in range(count):
            q_data = self.qgen_agent.generate_question(
                role=role,
                difficulty=difficulty,
                answered_questions=answered,
                skills=skills
            )
            if q_data:
                questions.append(q_data)
                answered.add(q_data["raw_question"])
        return questions

    def get_adaptive_difficulty(self, current_difficulty, history):
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

    def generate_followup(self, question, expected_answer, user_answer, role="Engineering Candidate"):
        return self.followup_agent.generate_followup(question, expected_answer, user_answer, role=role)

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
