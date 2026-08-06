import os
import random
import requests
import re
from rag_pipeline.rag import RAGPipeline

class OllamaClient:
    def __init__(self, model="mistral", host="http://localhost:11434"):
        self.model = model
        self.host = host
        self.is_connected = self.check_connection()

    def check_connection(self):
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=2)
            if response.status_code == 200:
                print(f"[Ollama] Connected successfully. Model: {self.model}")
                return True
        except Exception:
            pass
        print("[Ollama] Local Ollama service is not running. Switching to Simulated LLM Engine.")
        return False

    def generate(self, prompt, temperature=0.7):
        if not self.is_connected:
            return None
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature
                }
            }
            response = requests.post(f"{self.host}/api/generate", json=payload, timeout=15)
            if response.status_code == 200:
                return response.json().get("response", "").strip()
        except Exception as e:
            print(f"[Ollama Error] generation failed: {e}")
        return None

# Map of follow-up questions for fallback mode when LLM is unavailable
FALLBACK_FOLLOWUPS = {
    "list and tuple": "Under what specific production scenarios would you prefer using a tuple over a list to optimize performance?",
    "memory managed": "Can you explain how reference counting handles memory cleanups, and when does Python's cyclical garbage collector step in?",
    "decorators": "How would you create a decorator that accepts custom arguments, and how does functools.wraps help preserve metadata?",
    "deep copy and shallow copy": "What are the performance differences between deepcopy() and copy(), and what happens when copying objects containing database connections?",
    "generator functions": "How does calling next() on a generator update its instruction pointer under the hood, and how can we send values back into a generator?",
    "join": "What is a hash join or merge join, and how does the database optimizer choose which join algorithm to apply?",
    "sql injection": "How do parameterized queries secure databases, and why does validating inputs on the frontend not prevent injection?",
    "where and having": "Why does aggregating data before a WHERE clause raise a syntax error, and what are the performance impacts of filtering in HAVING?",
    "indexes": "What is the difference between a clustered index and a non-clustered index, and how does index fragmentation occur?",
    "etl and elt": "In cloud environments, what are the cost and performance advantages of running transformation tasks inside Snowflake or BigQuery (ELT)?",
    "spark": "Explain Spark partitions. How does shuffling occur during a groupByKey or reduceByKey operation, and how do we prevent it?",
    "kafka": "What is offset commit management, and how do consumer groups coordinate to rebalance partitions when a broker fails?",
    "star schema": "What is a slowly changing dimension (SCD), and how do you design a star schema to handle historical changes (SCD Type 2)?",
    "supervised": "Can you describe a scenario where you would choose an unsupervised clustering algorithm as a preprocessing step for a supervised model?",
    "bias-variance": "If you observe high training accuracy but low validation accuracy, is the model suffering from high bias or high variance? How do you resolve this?",
    "overfitting": "How does L1 Lasso regularization differ from L2 Ridge in terms of coefficient shrinking, and why does Lasso perform feature selection?"
}

class QuestionGeneratorAgent:
    def __init__(self, rag_pipeline: RAGPipeline, ollama_client: OllamaClient):
        self.rag = rag_pipeline
        self.ollama = ollama_client

    def generate_question(self, role, difficulty, answered_questions, skills=None):
        """
        Generates/retrieves the next interview question.
        Uses similarity search on the candidate's skills to prioritize questions.
        """
        query_str = " ".join(skills) if skills else "core concepts"
        
        # Retrieve candidate questions from vector DB
        retrieved = self.rag.retrieve_questions(
            role=role,
            difficulty=difficulty,
            query=query_str,
            k=10
        )

        # Filter out questions that have already been asked in this session
        available = [r for r in retrieved if r["question"] not in answered_questions]
        
        if not available:
            # Fallback if all matches are asked: retrieve without skill queries
            fallback_retrieved = self.rag.retrieve_questions(role=role, difficulty=difficulty, k=15)
            available = [r for r in fallback_retrieved if r["question"] not in answered_questions]

        if not available:
            # Absolute fallback if we run out of matching difficulty questions
            fallback_retrieved = self.rag.retrieve_questions(role=role, k=20)
            available = [r for r in fallback_retrieved if r["question"] not in answered_questions]

        if not available:
            return None

        # Select the best matching question
        selected = available[0]

        # If Ollama is active, we can refine the question text to make it conversational
        if self.ollama.is_connected:
            prompt = (
                f"You are a professional technical interviewer conducting an interview for a {role} role at {difficulty} difficulty.\n"
                f"Here is the technical topic: {selected['topic']}.\n"
                f"Introduce the question naturally, as if in a real conversation. Do not add numbering or boilerplate.\n"
                f"The question to ask: {selected['question']}"
            )
            refined = self.ollama.generate(prompt)
            if refined:
                return {
                    "question": refined,
                    "raw_question": selected["question"],
                    "expected_answer": selected["answer"],
                    "topic": selected["topic"],
                    "difficulty": selected["difficulty"]
                }

        # Otherwise return directly
        return {
            "question": selected["question"],
            "raw_question": selected["question"],
            "expected_answer": selected["answer"],
            "topic": selected["topic"],
            "difficulty": selected["difficulty"]
        }


class AnswerEvaluatorAgent:
    def __init__(self, ollama_client: OllamaClient):
        self.ollama = ollama_client

    def evaluate_answer(self, question, expected_answer, user_answer):
        """
        Evaluates the candidate's answer against the expected answer.
        Returns a score (1-10) and feedback.
        """
        if not user_answer or len(user_answer.strip()) < 5:
            return {
                "score": 1.0,
                "feedback": "No answer was provided, or the answer was too short to evaluate. Please try explaining the key terms and concepts."
            }

        # 1. Live LLM Evaluation
        if self.ollama.is_connected:
            prompt = (
                f"You are an expert technical interviewer. Evaluate the candidate's answer to the question below.\n\n"
                f"Question: {question}\n"
                f"Reference Answer: {expected_answer}\n"
                f"Candidate's Answer: {user_answer}\n\n"
                f"Provide a rigorous evaluation. You must respond in a structured format:\n"
                f"Score: <integer score from 1 to 10>\n"
                f"Feedback: <brief 2-3 sentence qualitative feedback explaining what is correct, what is missing, and how to improve>"
            )
            response = self.ollama.generate(prompt)
            if response:
                # Parse score and feedback
                score_match = re.search(r'Score:\s*(\d+)', response, re.IGNORECASE)
                feedback_match = re.search(r'Feedback:\s*(.*)', response, re.IGNORECASE | re.DOTALL)
                
                score = float(score_match.group(1)) if score_match else 5.0
                feedback = feedback_match.group(1).strip() if feedback_match else response
                return {
                    "score": min(max(score, 1.0), 10.0),
                    "feedback": feedback
                }

        # 2. Offline Semantic/Keyword Matching Fallback
        # Tokenize and extract key terms from both expected and candidate answers
        expected_words = set(re.findall(r'\b\w{4,}\b', expected_answer.lower()))
        user_words = set(re.findall(r'\b\w{4,}\b', user_answer.lower()))

        # Remove common english stopwords
        stopwords = {"with", "that", "this", "they", "them", "from", "their", "will", "would", "about", "there", "these", "which", "could", "should"}
        expected_keywords = expected_words - stopwords
        
        # Calculate overlap
        matched_keywords = expected_keywords.intersection(user_words)
        overlap_ratio = len(matched_keywords) / len(expected_keywords) if expected_keywords else 0.0

        # Calculate a score based on keyword coverage and details
        # Length bonus: encourages elaborate explanations
        words_count = len(user_answer.split())
        length_factor = min(words_count / 40.0, 1.0) # Full length credit at 40 words
        
        score = 1.0 + (overlap_ratio * 7.0) + (length_factor * 2.0)
        score = round(min(max(score, 1.0), 10.0), 1)

        # Generate custom feedback based on matched/unmatched keywords
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
    def __init__(self, ollama_client: OllamaClient):
        self.ollama = ollama_client

    def generate_followup(self, question, expected_answer, user_answer):
        """
        Generates a follow-up question to dive deeper.
        """
        # 1. Live LLM Follow-Up
        if self.ollama.is_connected:
            prompt = (
                f"You are a technical interviewer. The candidate has answered a question, but their answer was partially incomplete or can be expanded.\n"
                f"Question asked: {question}\n"
                f"Reference Answer: {expected_answer}\n"
                f"Candidate's Answer: {user_answer}\n\n"
                f"Generate exactly one short, conversational follow-up question related to their explanation. Do not add intro/outro boilerplate."
            )
            followup = self.ollama.generate(prompt)
            if followup:
                return followup

        # 2. Offline Fallback Mapping
        text = question.lower()
        for key, followup_q in FALLBACK_FOLLOWUPS.items():
            if any(k in text for k in key.split()):
                return followup_q
                
        # General generic fallback if no keyword matches
        return "Could you elaborate on the practical implementation challenges or trade-offs of this approach in a production environment?"


class FeedbackAgent:
    def __init__(self, ollama_client: OllamaClient):
        self.ollama = ollama_client

    def generate_report(self, role, history):
        """
        Generates the final comprehensive interview report.
        """
        total_questions = len(history)
        if total_questions == 0:
            return "No interview history recorded."

        average_score = sum(item["score"] for item in history) / total_questions
        average_score = round(average_score, 1)

        # Categorize by topic performance
        topic_scores = {}
        for item in history:
            topic = item["topic"]
            if topic not in topic_scores:
                topic_scores[topic] = []
            topic_scores[topic].append(item["score"])

        topic_perf = {}
        for topic, scores in topic_scores.items():
            topic_perf[topic] = round(sum(scores) / len(scores), 1)

        # 1. Live LLM Report
        if self.ollama.is_connected:
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
                f"Please format your response strictly in markdown with sections: "
                f"## Executive Summary, ## Topic-wise Breakdown, ## Key Strengths, ## Areas for Improvement, ## Overall Recommendation."
            )
            report = self.ollama.generate(prompt)
            if report:
                return report

        # 2. Offline Fallback Report Generation
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
            report += "The candidate exhibits excellent technical proficiency and is highly recommended for advanced engineering roles. They write clear explanations and cover architectural aspects."
        elif average_score >= 6.0:
            report += "The candidate has a solid foundation and can handle standard engineering tasks. They should focus on strengthening their understanding in areas tagged as 'Developing' before entering production projects."
        else:
            report += "The candidate requires further preparation in foundational principles. Focus on building core projects and reviewing standard interview guides before re-applying."

        return report
