"""
Base Scraper Framework

Purpose:
Provide a common interface for all scraper implementations.

Future scraper types:

* InterviewQuestionScraper
* JobDescriptionScraper
* DocumentationScraper
* ExperienceScraper

All scraper classes should inherit from BaseScraper.
"""

class BaseScraper:

# Base class for all scraper implementations.

# ```
# Every scraper should follow the same workflow:

# Fetch Page
#     ↓
# Parse Content
#     ↓
# Clean Text
#     ↓
# Save Data

    def fetch_page(self):
        """
        Fetch webpage content.

        To be implemented by child classes.
        """
        pass

    def parse_content(self):
        """
        Extract useful information from raw content.

        To be implemented by child classes.
        """
        pass

    def clean_text(self):
        """
        Clean extracted content.

        Examples:
        - Remove extra spaces
        - Remove HTML artifacts
        - Standardize formatting

        To be implemented by child classes.
        """
        pass

    def save_data(self):
        """
        Save processed data to storage.

        Examples:
        - TXT files
        - CSV files
        - JSON files

        To be implemented by child classes.
        """
        pass
