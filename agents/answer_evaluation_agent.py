"""
Answer Evaluation Agent

Purpose:
Evaluate candidate answers using
TF-IDF Vectorization and Cosine Similarity.

Pipeline:

Expected Answer
        ↓
TF-IDF Vectorization
        ↓
Cosine Similarity
        ↓
Score
        ↓
Feedback
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class AnswerEvaluationAgent:
    """
    Agent responsible for evaluating
    candidate answers using NLP techniques.
    """

    def similarity_to_score(self, similarity: float) -> int:
        """
        Convert cosine similarity (0-1)
        into a score (0-100).
        """
        return round(similarity * 100)

    def generate_feedback(self, score: int) -> str:
        """
        Generate qualitative feedback
        based on the calculated score.
        """

        if score >= 80:
            return (
                "Excellent answer. Strong understanding of concepts."
            )

        elif score >= 60:
            return (
                "Good understanding. Some details could be improved."
            )

        elif score >= 40:
            return (
                "Partial understanding. Important concepts are missing."
            )

        return (
            "Weak answer. Review the topic and key concepts."
        )

    def evaluate_answer(
        self,
        expected_answer: str,
        candidate_answer: str,
    ):
        """
        Evaluate the candidate answer using
        TF-IDF Vectorization and Cosine Similarity.
        """

        # Handle empty answer
        if not candidate_answer.strip():
            return {
                "score": 0,
                "similarity": 0.0,
                "feedback": "No answer provided.",
            }

        vectorizer = TfidfVectorizer()

        vectors = vectorizer.fit_transform(
            [
                expected_answer,
                candidate_answer,
            ]
        )

        similarity = cosine_similarity(
            vectors[0:1],
            vectors[1:2],
        )[0][0]

        score = self.similarity_to_score(similarity)

        feedback = self.generate_feedback(score)

        return {
            "score": score,
            "similarity": round(similarity, 4),
            "feedback": feedback,
        }


if __name__ == "__main__":

    expected_answer = (
        "Python is a high-level interpreted programming language."
    )

    candidate_answer = (
        "Python is an interpreted programming language."
    )

    agent = AnswerEvaluationAgent()

    result = agent.evaluate_answer(
        expected_answer=expected_answer,
        candidate_answer=candidate_answer,
    )

    print("\nAnswer Evaluation Result")
    print("-" * 35)
    print(f"Score      : {result['score']}")
    print(f"Similarity : {result['similarity']}")
    print(f"Feedback   : {result['feedback']}")