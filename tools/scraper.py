import feedparser
import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
from configuration.config import RSS_FEED_URL

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_rss_feed() -> list:
    """
    Downloads and parses the RSS feed from the specified URL.
    
    Returns:
        list: List of RSS feed entries, each entry is a dictionary containing article information.
    """
    try:
        logger.info(f"Feed RSS download from {RSS_FEED_URL}")
        feed = feedparser.parse(RSS_FEED_URL)

        if not feed.entries:
            logger.warning("No entries found in the RSS feed")
            return []

        logger.info(f"{len(feed.entries)} articles found in the RSS feed")
        return feed.entries
    except Exception as e:
        logger.error(f"Error during the RSS feed parsing: {e}")
        return []

def get_article_content(url) -> str:
    """
    Downloads the content of an article from the given URL.
    
    Args:
        url (str): URL of the article to download
        
    Returns:
        str: The text content of the article, cleaned and formatted.
    """
    try:
        logger.info(f"Downloading article content from {url}")
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
        logger.error(f"Error while downloading article content: {e}")
        return ""

def collect_articles() -> list:
    """
    Recovers articles from the RSS feed and downloads their content.
    
    Returns:
        list: List of dictionaries, each containing information about an article.
    """
    articles = []
    entries = parse_rss_feed()

    for entry in entries:
        try:
            article = {
                'title': entry.title,
                'link': entry.link,
                'published': entry.published,
                'summary': entry.summary if hasattr(entry, 'summary') else "",
                'content': get_article_content(entry.link),
                'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            articles.append(article)
            logger.info(f"Article collected: {article['title']}")
        except Exception as e:
            logger.error(f"Error while processing article '{entry.title}': {e}")

    return articles