"""
Module name: ner.py
Author: Michele Grieco
Description:
    This module provides a Named Entity Recognition (NER) system using SpaCy. It includes functionalities to extract named entities from text,
    verify the presence of a specific company, and retrieve mentions of that company with context.
Usage:
    from tools.ner import NamedEntityRecognizer

    ner = NamedEntityRecognizer()
    text = "Apple is looking at buying U.K. startup for $1 billion"
    
    # Extract entities
    entities = ner.extract_entities(text)
    print(entities)
    
    # Check if a specific company is mentioned
    is_mentioned = ner.is_company_mentioned(text, company="Apple")
    print(is_mentioned)
    
    # Get mentions of a specific company with context
    mentions = ner.get_company_mentions(text, company="Apple")
    print(mentions)
"""

import spacy # for NLP and NER
from spacy.cli.download import download # for downloading SpaCy models
import logging
from configuration.config import SPACY_MODEL, TARGET_COMPANY

class NamedEntityRecognizer:
    """
    A class for performing Named Entity Recognition (NER) using SpaCy.
    """
    
    def __init__(self, model_name=SPACY_MODEL) -> None:
        """
        Initialize the NER system with a specific SpaCy model.
        
        Args:
            model_name (str): Name of the SpaCy model to use
        """
        # Logger configuration
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Initialize SpaCy model
        self.nlp = self._initialize_spacy_model(model_name)

    def _initialize_spacy_model(self, model_name) -> spacy.language.Language:
        """
        Initialize the SpaCy model with fallback options.
        
        Args:
            model_name (str): Name of the SpaCy model to load
            
        Returns:
            spacy.language.Language: Loaded SpaCy model
        """
        try:
            nlp = spacy.load(model_name)
            self.logger.info(f"SpaCy model {model_name} successfully loaded for NER")
            return nlp
        except Exception as e:
            self.logger.error(f"Error during SpaCy loading for NER: {e}")
            self.logger.info("SpaCy model not found, attempting to download...")
            try:
                download(model_name)
                nlp = spacy.load(model_name)
                self.logger.info(f"SpaCy model {model_name} downloaded and loaded successfully for NER")
                return nlp
            except Exception as e:
                self.logger.error(f"Error during SpaCy model download or loading: {e}")
                raise

    def extract_entities(self, text) -> list:
        """
        Extract named entities from the given text using SpaCy NER.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            list: List of tuples containing entity text and its label
        """
        if not text:
            return []

        self.logger.info("Extracting entities from text using SpaCy NER")
        doc = self.nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        self.logger.info(f"{len(entities)} entities extracted from text")
        return entities

    def is_company_mentioned(self, text, company=TARGET_COMPANY) -> bool:
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
            self.logger.info(f"Company {company} found in text without NER")
            return True

        # Verification using NER
        entities = self.extract_entities(text)

        # Search for the company in the extracted entities
        for entity, entity_type in entities:
            if (company.lower() in entity.lower()) and (entity_type in ['ORG', 'ORGANIZATION', 'PRODUCT', 'COMPANY']):
                self.logger.info(f"Company {company} found with NER as {entity_type}")
                return True

        self.logger.info(f"Company {company} not found in text")
        return False

    def get_company_mentions(self, text, company=TARGET_COMPANY) -> list:
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

        doc = self.nlp(text)
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

        self.logger.info(f"Found {len(mentions)} mentions of company {company} in text")
        return mentions