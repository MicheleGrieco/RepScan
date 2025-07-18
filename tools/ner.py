# Named Entity Recognition (NER) with SpaCy
import spacy
from spacy.cli.download import download
import logging
from configuration.config import SPACY_MODEL, TARGET_COMPANY

# Logger configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Loads SpaCy model
try:
    nlp = spacy.load(SPACY_MODEL)
    logger.info(f"SpaCy model {SPACY_MODEL} successfully loaded for NER")
except Exception as e:
    logger.error(f"Error during SpaCy loading for NER: {e}")
    logger.info("SpaCy model not found, attempting to download...")
    try:
        download(SPACY_MODEL)
        nlp = spacy.load(SPACY_MODEL)
        logger.info(f"SpaCy model {SPACY_MODEL} downloaded and loaded successfully for NER")
    except Exception as e:
        logger.error(f"Impossibile scaricare il modello SpaCy per NER: {e}")
        raise

def extract_entities(text):
    """
    Estrae le entità nominate dal testo utilizzando SpaCy
    
    Args:
        text (str): Testo da analizzare
        
    Returns:
        list: Lista di tuple (entità, tipo)
    """
    if not text:
        return []

    logger.info("Iniziata l'estrazione delle entità")

    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    logger.info(f"Estratte {len(entities)} entità dal testo")
    return entities

def is_company_mentioned(text, company=TARGET_COMPANY):
    """
    Verifica se l'azienda target è menzionata nel testo
    
    Args:
        text (str): Testo da analizzare
        company (str): Nome dell'azienda da cercare
        
    Returns:
        bool: True se l'azienda è menzionata, False altrimenti
    """
    if not text:
        return False

    # Verifica semplice con ricerca di stringhe
    if company.lower() in text.lower():
        logger.info(f"Azienda {company} trovata con ricerca semplice")
        return True

    # Verifica con NER
    entities = extract_entities(text)

    # Cerca l'azienda tra le entità
    for entity, entity_type in entities:
        if (company.lower() in entity.lower()) and (entity_type in ['ORG', 'ORGANIZATION', 'PRODUCT', 'COMPANY']):
            logger.info(f"Azienda {company} trovata con NER come {entity_type}")
            return True

    logger.info(f"Azienda {company} non trovata nel testo")
    return False

def get_company_mentions(text, company=TARGET_COMPANY):
    """
    Restituisce tutte le menzioni dell'azienda nel testo
    
    Args:
        text (str): Testo da analizzare
        company (str): Nome dell'azienda da cercare
        
    Returns:
        list: Lista di menzioni dell'azienda
    """
    if not text:
        return []

    doc = nlp(text)
    mentions = []

    # Cerca menzioni dell'azienda nelle entità
    for ent in doc.ents:
        if (company.lower() in ent.text.lower()) and (ent.label_ in ['ORG', 'ORGANIZATION', 'PRODUCT', 'COMPANY']):
            context_start = max(0, ent.start_char - 50)
            context_end = min(len(text), ent.end_char + 50)
            context = text[context_start:context_end]
            mentions.append({
                'text': ent.text,
                'context': context,
                'type': ent.label_
            })

    logger.info(f"Trovate {len(mentions)} menzioni dell'azienda {company}")
    return mentions