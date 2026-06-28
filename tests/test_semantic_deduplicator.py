import pandas as pd

from knowledge_base.semantic_deduplicator import (
    SemanticDeduplicator
)


def test_duplicate_detection():

    deduplicator = (
        SemanticDeduplicator(
            threshold=0.70
        )
    )

    deduplicator.dataset = pd.DataFrame(
        {
            "question": [
                "What is Python?",
                "Explain Python language.",
                "What is Kafka?"
            ]
        }
    )

    deduplicator.generate_embeddings()

    duplicates = (
        deduplicator.find_duplicates()
    )

    assert len(duplicates) >= 1


def test_remove_duplicates():

    deduplicator = (
        SemanticDeduplicator(
            threshold=0.70
        )
    )

    deduplicator.dataset = pd.DataFrame(
        {
            "question": [
                "What is Python?",
                "Explain Python language.",
                "What is Kafka?"
            ]
        }
    )

    deduplicator.generate_embeddings()

    cleaned = (
        deduplicator.remove_duplicates()
    )

    assert len(cleaned) <= 3


def test_similarity_threshold():

    deduplicator = (
        SemanticDeduplicator(
            threshold=0.90
        )
    )

    assert (
        deduplicator.threshold
        == 0.90
    )