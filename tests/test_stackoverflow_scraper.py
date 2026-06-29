from scraper.stackoverflow_scraper import (
    StackOverflowScraper,
)


def test_scraper_creation():

    scraper = (
        StackOverflowScraper()
    )

    assert scraper is not None


def test_supported_tags():

    scraper = (
        StackOverflowScraper()
    )

    assert (
        "python"
        in scraper.TAGS
    )


def test_parse_questions():

    scraper = (
        StackOverflowScraper()
    )

    mock_response = {
    "items": [
        {
            "title":
                "What is Python?",

            "body":
                (
                    "Explain Python programming "
                    "language and its features."
                ),

            "tags":
                ["python"],

            "score":
                100,

            "accepted_answer":
                (
                    "Python is a high-level "
                    "interpreted programming "
                    "language widely used in "
                    "software development."
                ),

            "accepted_answer_id":
                12345,

            "link":
                "https://stackoverflow.com",
        }
    ]
}

    records = (
        scraper.parse_questions(
            mock_response
        )
    )

    assert len(records) == 1

    assert (
        records[0]["question"]
        == "What is Python?"
    )