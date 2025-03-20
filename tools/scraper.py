import feedparser
import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
from config import RSS_FEED_URL

# Configurazione del logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_rss_feed():
    """
    Scarica e analizza il feed RSS specificato in config.py
    
    Returns:
        list: Lista di dizionari, ciascuno contenente le informazioni di un articolo
    """
    try:
        logger.info(f"Scaricamento del feed RSS da {RSS_FEED_URL}")
        feed = feedparser.parse(RSS_FEED_URL)

        if not feed.entries:
            logger.warning("Nessun articolo trovato nel feed RSS")
            return []

        logger.info(f"Trovati {len(feed.entries)} articoli nel feed RSS")
        return feed.entries
    except Exception as e:
        logger.error(f"Errore durante il parsing del feed RSS: {e}")
        return []

def get_article_content(url):
    """
    Scarica il contenuto completo di un articolo dalla sua URL
    
    Args:
        url (str): URL dell'articolo
        
    Returns:
        str: Contenuto testuale dell'articolo
    """
    try:
        logger.info(f"Scaricamento del contenuto dell'articolo da {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Rimuovi script e stili
        for script_or_style in soup(['script', 'style']):
            script_or_style.decompose()

        # Ottieni il testo
        text = soup.get_text()

        # Pulizia base
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return text
    except Exception as e:
        logger.error(f"Errore durante il recupero del contenuto dell'articolo: {e}")
        return ""

def collect_articles():
    """
    Raccoglie gli articoli dal feed RSS e scarica il loro contenuto
    
    Returns:
        list: Lista di dizionari contenenti le informazioni degli articoli
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
            logger.info(f"Articolo raccolto: {article['title']}")
        except Exception as e:
            logger.error(f"Errore durante la raccolta dell'articolo: {e}")

    return articles