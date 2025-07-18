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
        logger.error(f"Error during SpaCy model download or loading: {e}")
        raise

def extract_entities(text) -> list:
    """
    Extract named entities from the given text using SpaCy NER.
    
    Args:
        text (str): Text to analyze
        
    Returns:
        list: List of tuples containing entity text and its label
    """
    if not text:
        return []

    logger.info("Extracting entities from text using SpaCy NER")

    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    logger.info(f"{len(entities)} entities extracted from text")
    return entities

def is_company_mentioned(text, company=TARGET_COMPANY) -> bool:
    """
    Verifies if a specific company is mentioned in the text.
    
    Args:
        text (str): Text to analyze
        company (str): Company name to search for
        
    Returns:
        bool: True if the company is mentioned, False otherwise
    """
    if not text:
        return False

    # Simple search for the company name
    if company.lower() in text.lower():
        logger.info(f"Company {company} found in text without NER")
        return True

    # Verification using NER
    entities = extract_entities(text)

    # Search for the company in the extracted entities
    for entity, entity_type in entities:
        if (company.lower() in entity.lower()) and (entity_type in ['ORG', 'ORGANIZATION', 'PRODUCT', 'COMPANY']):
            logger.info(f"Company {company} found with NER as {entity_type}")
            return True

    logger.info(f"Company {company} not found in text")
    return False

def get_company_mentions(text, company=TARGET_COMPANY) -> list:
    """
    Retrieve mentions of a specific company in the text.
    
    Args:
        text (str): Text to analyze
        company (str): Company name to search for
        
    Returns:
        list: List of mentions with context and type
    """
    if not text:
        return []

    doc = nlp(text)
    mentions = []

    # Search for company mentions in the entities
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

    logger.info(f"Found {len(mentions)} mentions of company {company} in text")
    return mentions