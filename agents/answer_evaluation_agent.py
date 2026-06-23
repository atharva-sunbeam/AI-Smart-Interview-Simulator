"""
Answer Evaluation Agent

Purpose:
Evaluate candidate answers using
TF-IDF vectorization and Cosine Similarity.

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

    
    def evaluate_answer(
        self,
        expected_answer: str,
        candidate_answer: str,
    ):
        """
        Evaluate candidate answer using
        cosine similarity.
        """

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

        score = round(similarity * 100)

        if score >= 80:
            feedback = (
                "Excellent answer. Strong understanding of concepts."
            )
        elif score >= 60:
            feedback = (
                "Good understanding. Some details could be improved."
            )
        elif score >= 40:
            feedback = (
                "Partial understanding. Important concepts are missing."
            )
        else:
            feedback = (
                "Weak answer. Review the topic and key concepts."
            )

        return {
            "score": score,
            "feedback": feedback,
        }
    

if __name__ == "__main__":


    agent = AnswerEvaluationAgent()

    result = agent.evaluate_answer(
        expected_answer=(
            "Python is a high-level interpreted programming language."
        ),
        candidate_answer=(
            "Python is an interpreted programming language."
        ),
    )

    print(result)
    
