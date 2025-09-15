"""
Module name: preprocess.py
Author: Michele Grieco
Description:
    This module provides a TextPreprocessor class for preprocessing text data, including removing HTML tags, URLs,
    special characters, and stopwords. It utilizes the SpaCy library for natural language processing tasks.
    It is designed to handle Italian text and can be easily extended for other languages by changing the SpaCy model.
Usage:
    from preprocess import TextPreprocessor
    preprocessor = TextPreprocessor()
    cleaned_text = preprocessor.preprocess(raw_text, remove_stops=True)
"""

import re # for regular expressions
import unicodedata # for Unicode normalization
import spacy # for NLP tasks
from spacy.cli.download import download
import logging 
from bs4 import BeautifulSoup # for HTML tag removal
from configuration.config import SPACY_MODEL

class TextPreprocessor:
    """
    A class for preprocessing text data, including removing HTML tags, URLs, special characters, and stopwords.
    """
    
    def __init__(self, model_name: str = SPACY_MODEL) -> None:
        """
        Initialize the TextPreprocessor with a specific SpaCy model.
        
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

    def _initialize_spacy_model(self, model_name: str) -> spacy.language.Language:
        """
        Initialize the SpaCy model with fallback options.
        
        Args:
            model_name (str): Name of the SpaCy model to load
            
        Returns:
            spacy.language.Language: Loaded SpaCy model
        """
        try:
            nlp = spacy.load(model_name)
            self.logger.info(f"SpaCy model {model_name} successfully loaded")
            return nlp
        except Exception as e:
            self.logger.error(f"Error during SpaCy model loading: {e}")
            self.logger.info("SpaCy model not found, attempting to download...")
            try:
                download(model_name)
                nlp = spacy.load(model_name)
                self.logger.info(f"SpaCy model {model_name} downloaded and loaded successfully")
                return nlp
            except Exception as e:
                self.logger.error(f"Unable to download SpaCy model {e}")
                try:
                    nlp = spacy.blank("it")
                    self.logger.info("Loaded blank SpaCy model as fallback.")
                    return nlp
                except:
                    self.logger.critical("Importing SpaCy model failed, please check your installation and model name.")
                    raise

    def remove_html_tags(self, text: str) -> str:
        """
        Remove HTML tags from the text
        Args:
            text (str): Text from which to remove HTML tags
        Returns:
            str: Text without HTML tags
        """
        return BeautifulSoup(text, "html.parser").get_text()

    def remove_urls(self, text) -> str:
        """
        Remove URLs from the text
        Args:
            text (str): Text from which to remove URLs
        Returns:
            str: Text without URLs
        """
        url_pattern = re.compile(r'https?://\S+|www\.\S+')
        return url_pattern.sub('', text)

    def remove_special_chars(self, text: str) -> str:
        """
        Remove special characters from the text and normalize it
        Args:
            text (str): Text from which to remove special characters
        Returns:
            str: Cleaned and normalized text
        """
        text = unicodedata.normalize('NFKD', text)
        text = re.sub(r'[^\w\s\.,;:!?]', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def remove_stopwords(self, text: str) -> str:
        """
        Remove stopwords from the text using SpaCy
        Args:
            text (str): Text from which to remove stopwords
        Returns:
            str: Text without stopwords
        """
        doc = self.nlp(text)
        filtered_tokens = [token.text for token in doc if not token.is_stop]
        return ' '.join(filtered_tokens)

    def preprocess(self, text, remove_stops: bool = False) -> str:
        """
        Execute all preprocessing steps on the input text.
        
        Args:
            text (str): Text to preprocess
            remove_stops (bool): Whether to remove stopwords
            
        Returns:
            str: Preprocessed text
        """
        if not text:
            return ""

        self.logger.info("Text preprocessing started")

        text = self.remove_html_tags(text)
        text = self.remove_urls(text)
        text = self.remove_special_chars(text)

        if remove_stops:
            text = self.remove_stopwords(text)

        self.logger.info("Text preprocessing completed")
        return text