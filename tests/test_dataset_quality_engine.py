from knowledge_base.dataset_quality_engine import (
    DatasetQualityEngine,
)


def test_remove_html():

    engine = DatasetQualityEngine()

    text = "<b>Hello</b> &amp; Welcome"

    assert (
        engine.remove_html(text)
        == "Hello & Welcome"
    )


def test_quality_score():

    engine = DatasetQualityEngine()

    record = {
        "question":
            "What is Python?",

        "answer":
            "Python is a high-level programming language used in web development, data science, automation, machine learning, and scripting.",

        "score":
            150,

        "accepted_answer":
            "123",
    }

    quality = engine.assign_quality_score(
        record
    )

    assert quality > 0


def test_filter_records():

    engine = DatasetQualityEngine()

    records = [
        {
            "question":
                "What is Python?",

            "answer":
                "Python is a high-level interpreted programming language used for software development, automation, AI, and data science.",

            "score":
                50,

            "accepted_answer":
                (
                    "Python is a high-level "
                    "programming language used "
                    "for multiple domains."
                ),
        }
    ]

    filtered = engine.filter_records(
        records
    )

    assert len(filtered) == 1
