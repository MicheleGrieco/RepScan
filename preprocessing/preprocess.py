import re
import unicodedata
import spacy
import logging
from bs4 import BeautifulSoup
from configuration.config import SPACY_MODEL

# Configurazione del logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Carica il modello SpaCy per le stopwords
try:
    nlp = spacy.load(SPACY_MODEL)
    logger.info(f"Modello SpaCy {SPACY_MODEL} caricato con successo")
except Exception as e:
    logger.error(f"Errore durante il caricamento del modello SpaCy: {e}")
    logger.info("Tentativo di download del modello SpaCy")
    try:
        spacy.cli.download(SPACY_MODEL)
        nlp = spacy.load(SPACY_MODEL)
        logger.info(f"Modello SpaCy {SPACY_MODEL} scaricato e caricato con successo")
    except Exception as e:
        logger.error(f"Impossibile scaricare il modello SpaCy: {e}")
        # Fallback a un modello più piccolo
        try:
            nlp = spacy.blank("it")
            logger.info("Caricato modello SpaCy vuoto come fallback")
        except:
            logger.critical("Impossibile caricare alcun modello SpaCy")
            raise

def remove_html_tags(text):
    """
    Rimuove i tag HTML dal testo
    
    Args:
        text (str): Testo con possibili tag HTML
        
    Returns:
        str: Testo pulito dai tag HTML
    """
    return BeautifulSoup(text, "html.parser").get_text()

def remove_urls(text):
    """
    Rimuove gli URL dal testo
    
    Args:
        text (str): Testo con possibili URL
        
    Returns:
        str: Testo pulito dagli URL
    """
    # Pattern per riconoscere gli URL
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub('', text)

def remove_special_chars(text):
    """
    Rimuove caratteri speciali e normalizza il testo
    
    Args:
        text (str): Testo da pulire
        
    Returns:
        str: Testo normalizzato
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
    Rimuove le stopwords dal testo
    
    Args:
        text (str): Testo da cui rimuovere le stopwords
        
    Returns:
        str: Testo senza stopwords
    """
    doc = nlp(text)
    filtered_tokens = [token.text for token in doc if not token.is_stop]
    return ' '.join(filtered_tokens)

def preprocess_text(text, remove_stops=False):
    """
    Esegue tutti i passaggi di preprocessing sul testo
    
    Args:
        text (str): Testo da preprocessare
        remove_stops (bool): Se True, rimuove le stopwords
        
    Returns:
        str: Testo preprocessato
    """
    if not text:
        return ""

    logger.info("Iniziato il preprocessing del testo")

    # Applica tutte le funzioni di preprocessing
    text = remove_html_tags(text)
    text = remove_urls(text)
    text = remove_special_chars(text)

    # Rimuovi stopwords solo se richiesto
    if remove_stops:
        text = remove_stopwords(text)

    logger.info("Preprocessing del testo completato")
    return text