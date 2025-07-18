import re
import unicodedata
import spacy
from spacy.cli.download import download
import logging
from bs4 import BeautifulSoup
from configuration.config import SPACY_MODEL

# Logger configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Loads the SpaCy model for Italian language processing
try:
    nlp = spacy.load(SPACY_MODEL)
    logger.info(f"SpaCy model {SPACY_MODEL} successfully loaded")
except Exception as e:
    logger.error(f"Error during SpaCy model loading: {e}")
    logger.info("SpaCy model not found, attempting to download...")
    try:
        download(SPACY_MODEL)
        nlp = spacy.load(SPACY_MODEL)
        logger.info(f"SpaCy model {SPACY_MODEL} downloaded and loaded successfully")
    except Exception as e:
        logger.error(f"Unable to download SpaCy model {e}")
        # Fallback a un modello più piccolo
        try:
            nlp = spacy.blank("it")
            logger.info("Loaded blank SpaCy model as fallback")
        except:
            logger.critical("Importing SpaCy model failed, please check your installation and model name.")
            raise

def remove_html_tags(text):
    """
    Remove HTML tags from the text
    
    Args:
        text (str): Text with possible HTML tags
        
    Returns:
        str: Text without HTML tags
    """
    return BeautifulSoup(text, "html.parser").get_text()

def remove_urls(text):
    """
    Remove URLs from the text
    
    Args:
        text (str): Text with possible URLs
        
    Returns:
        str: Text without URLs
    """
    # Pattern per riconoscere gli URL
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub('', text)

def remove_special_chars(text):
    """
    Removes special characters from the text, normalizes it, and removes extra spaces.
    
    Args:
        text (str): Text to be normalized
        
    Returns:
        str: Normalized text with special characters removed
    """
    # Normalizza in forma Unicode NFKD
    text = unicodedata.normalize('NFKD', text)

    # Rimuovi i caratteri non alfanumerici e mantieni spazi e punteggiatura principale
    text = re.sub(r'[^\w\s\.,;:!?]', '', text)

    # Rimuovi spazi multipli
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

def remove_stopwords(text):
    """
    Remove stopwords from the text using SpaCy.
    
    Args:
        text (str): Text from which to remove stopwords
        
    Returns:
        str: Text without stopwords
    """
    doc = nlp(text)
    filtered_tokens = [token.text for token in doc if not token.is_stop]
    return ' '.join(filtered_tokens)

def preprocess_text(text, remove_stops=False):
    """
    Executes the preprocessing steps on the input text.
    
    Args:
        text (str): Text to preprocess
        remove_stops (bool): True to remove stopwords, False otherwise
        
    Returns:
        str: Preprocessed text
    """
    if not text:
        return ""

    logger.info("Text preprocessing started")

    # Applica tutte le funzioni di preprocessing
    text = remove_html_tags(text)
    text = remove_urls(text)
    text = remove_special_chars(text)

    # Rimuovi stopwords solo se richiesto
    if remove_stops:
        text = remove_stopwords(text)

    logger.info("Text preprocessing completed")
    return text