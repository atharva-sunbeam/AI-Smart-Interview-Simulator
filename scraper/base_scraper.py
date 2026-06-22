"""
Base Scraper Framework

Purpose:
Provide reusable functionality for all scraper implementations.

Future scraper types:

* InterviewQuestionScraper
* JobDescriptionScraper
* DocumentationScraper
* ExperienceScraper

All scraper classes should inherit from BaseScraper.
"""

import requests

class BaseScraper:

# Base class for all scraper implementations.


# Common workflow:

# Fetch Page
#     ↓
# Parse Content
#     ↓
# Clean Text
#     ↓
# Save Data

    def get_page(self, url):
        """
        Fetch webpage content.

        Args:
            url (str): Target webpage URL

        Returns:
            str: Page content
        """

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        return response.text

    def save_to_file(self, filepath, data):
        """
        Save scraped data to a file.

        Args:
            filepath (str): Output file path
            data (str): Data to save
        """

        with open(filepath, "w", encoding="utf-8") as file:
            file.write(data)
