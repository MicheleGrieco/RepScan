"""
Module name: scraper.py
Author: Michele Grieco
Description:
    This module provides an ArticleScraper class for scraping articles from RSS feeds and downloading their content.
    It utilizes the feedparser and requests libraries for handling RSS feeds and HTTP requests, respectively.
    It is designed to be easily configurable via the configuration file.
Usage:
    from tools.scraper import ArticleScraper
    scraper = ArticleScraper()
    articles = scraper.collect_articles()
"""

import feedparser # for parsing RSS feeds
import requests # for HTTP requests
from bs4 import BeautifulSoup # for HTML parsing
import logging
from datetime import datetime
from configuration.config import RSS_FEED_URL

class ArticleScraper:
    """
    A class for scraping articles from RSS feeds and downloading their content.
    """
    
    def __init__(self, feed_url: str = RSS_FEED_URL):
        """
        Initialize the ArticleScraper with RSS feed URL and logging configuration.
        
        Args:
            feed_url (str): URL of the RSS feed to parse
        """
        self.feed_url = feed_url
        
        # Logger configuration
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def parse_rss_feed(self) -> list:
        """
        Download and parse the RSS feed from the specified URL.
        
        Returns:
            list: List of RSS feed entries
        """
        try:
            self.logger.info(f"Feed RSS download from {self.feed_url}")
            feed = feedparser.parse(self.feed_url)

            if not feed.entries:
                self.logger.warning("No entries found in the RSS feed")
                return []

            self.logger.info(f"{len(feed.entries)} articles found in the RSS feed")
            return feed.entries
        except Exception as e:
            self.logger.error(f"Error during the RSS feed parsing: {e}")
            return []

    def get_article_content(self, url: str) -> str:
        """
        Download the content of an article from the given URL.
        
        Args:
            url (str): URL of the article to download
            
        Returns:
            str: The text content of the article
        """
        try:
            self.logger.info(f"Downloading article content from {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove script and style elements
            for script_or_style in soup(['script', 'style']):
                script_or_style.decompose()

            # Extract text from the soup object
            text = soup.get_text()

            # Clean and format the text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)

            return text
        except Exception as e:
            self.logger.error(f"Error while downloading article content: {e}")
            return ""

    def collect_articles(self) -> list:
        """
        Recover articles from the RSS feed and download their content.
        
        Returns:
            list: List of dictionaries containing article information
        """
        articles = []
        entries = self.parse_rss_feed()

        for entry in entries:
            try:
                article = {
                    'title': entry.title,
                    'link': entry.link,
                    'published': entry.published,
                    'summary': entry.summary if hasattr(entry, 'summary') else "",
                    'content': self.get_article_content(entry.link),
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                articles.append(article)
                self.logger.info(f"Article collected: {article['title']}")
            except Exception as e:
                self.logger.error(f"Error while processing article '{entry.title}': {e}")

        return articles