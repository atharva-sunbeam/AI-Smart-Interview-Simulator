from bs4 import BeautifulSoup

from scraper.interview_question_scraper import (
InterviewQuestionScraper
)

class InterviewBitScraper(
InterviewQuestionScraper
):

# Prototype scraper for InterviewBit interview questions.


# Goal:
# Validate scraper architecture and data collection flow.

# Future improvements:
# - Better question extraction
# - Pagination support
# - Multiple categories
# - Duplicate removal


    def __init__(self):
        super().__init__()

        self.url = (
            "https://www.interviewbit.com/"
            "python-interview-questions/"
        )

    def fetch_questions(self):
        """
        Fetch page and extract candidate questions.

        Returns:
            list[str]
        """

        html = self.get_page(self.url)

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        questions = []

        headings = soup.find_all(
            ["h1", "h2", "h3"]
        )

        for heading in headings:
            text = heading.get_text(
                strip=True
            )

            if text:
                questions.append(text)

        return questions

