from scraper.gfg_scraper import (
    GFGScraper
)


def test_fetch_page():

    scraper = GFGScraper()

    html = scraper.fetch_page(
        (
            "https://www.geeksforgeeks.org/"
            "python-interview-questions/"
        )
    )

    assert html is not None
    assert len(html) > 0


def test_extract_questions():

    scraper = GFGScraper()

    sample_html = """
    <html>
        <body>

            <h2>
                What is Python?
            </h2>

            <p>
                Python is a programming language.
            </p>

            <h2>
                What is OOP?
            </h2>

            <p>
                OOP means Object Oriented Programming.
            </p>

        </body>
    </html>
    """

    records = (
        scraper.extract_questions_answers(
            sample_html,
            "https://example.com"
        )
    )

    assert len(records) == 2

    assert (
        records[0]["question"]
        == "What is Python?"
    )


def test_save_dataset():

    scraper = GFGScraper()

    records = [
        {
            "question":
                "What is Python?",

            "answer":
                "Python is a language.",

            "topic":
                "Python",

            "source":
                "GeeksforGeeks",

            "url":
                "https://example.com",

            "difficulty":
                "Easy"
        }
    ]

    scraper.save_dataset(
        records
    )

    assert True