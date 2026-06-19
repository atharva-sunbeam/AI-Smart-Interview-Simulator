"""
GeeksforGeeks Scraper

Purpose:
Collect interview questions and related technical content
from GeeksforGeeks.

Future Responsibilities:

* Fetch pages
* Parse interview questions
* Extract answers
* Save raw dataset
  """

from scraper.base_scraper import BaseScraper

class GFGScraper(BaseScraper):
    """
    Scraper for GeeksforGeeks interview content.
    """


    def __init__(self):
        pass

    def fetch_urls(self):
        """
        Load target URLs.
        """
        pass

    def scrape(self):
        """
        Main scraping workflow.
        """
        pass

    def parse_content(self, html):
        """
        Extract questions and answers.
        """
        pass

    def save_data(self, data):
        """
        Save extracted data.
        """
        pass
    
