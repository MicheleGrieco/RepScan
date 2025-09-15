#type: ignore

"""
Module name: sentiment_analysis.py
Author: Michele Grieco
Description:
    This module provides a class for sentiment analysis using transformer models. It includes methods for initializing the model,
    analyzing sentiment, and converting sentiment scores to labels.
    It also includes a fallback keyword-based sentiment analysis method in case the model fails to load.
    The module uses the Hugging Face transformers library.
Usage:
    from sentiment_analysis import SentimentAnalyzer

    analyzer = SentimentAnalyzer()
    score = analyzer.analyze_sentiment("Your text here")
    label = analyzer.get_sentiment_label(score)
"""

import logging
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from configuration.config import SENTIMENT_MODEL

class SentimentAnalyzer:
    """
    Class for sentiment analysis using transformer models
    """
    
    def __init__(self, model_name: str = SENTIMENT_MODEL) -> None:
        """
        Initialize the sentiment analyzer
        
        Args:
            model_name (str): Name of the model to use
        """
        self.logger = logging.getLogger(__name__)
        self.model_name = model_name
        self.sentiment_analyzer = self._initialize_model()
        
        # Keywords for fallback
        self.positive_words = ['ottimo', 'eccellente', 'positivo', 'buono', 'successo']
        self.negative_words = ['pessimo', 'negativo', 'cattivo', 'fallimento', 'problema']

    def _initialize_model(self) -> pipeline:
        """
        Initialize the sentiment analysis model
        
        Returns:
            pipeline: Transformers pipeline or None in case of error
        """
        try:
            analyzer = pipeline(
                "sentiment-analysis",
                model=self.model_name,
                tokenizer=self.model_name
            )
            self.logger.info(f"Sentiment analysis model {self.model_name} loaded successfully")
            return analyzer
        except Exception as e:
            self.logger.error(f"Error loading sentiment model: {str(e)}")
            return None

    def _fallback_analysis(self, text: str) -> float:
        """
        Keyword-based sentiment analysis (fallback)
        
        Args:
            text (str): Text to analyze
            
        Returns:
            float: Sentiment score between -1 and 1
        """
        self.logger.warning("Using keyword-based fallback sentiment analysis")
        text = text.lower()
        positive_count = sum(1 for word in self.positive_words if word in text)
        negative_count = sum(1 for word in self.negative_words if word in text)

        total = positive_count + negative_count
        if total == 0:
            return 0.0

        return (positive_count - negative_count) / total

    def analyze_sentiment(self, text: str) -> float:
        """
        Analyze the sentiment of the text
        
        Args:
            text (str): Text to analyze
            
        Returns:
            float: Sentiment score between -1 and 1
        """
        try:
            if self.sentiment_analyzer:
                # Limit text to maximum length
                max_length = 512
                if len(text) > max_length:
                    text = text[:max_length]

                result = self.sentiment_analyzer(text)

                # Convert result to a score between -1 and 1
                if result[0]['label'] == 'POSITIVE':
                    return result[0]['score']
                elif result[0]['label'] == 'NEGATIVE':
                    return -result[0]['score']
                else:
                    return 0.0
            else:
                return self._fallback_analysis(text)

        except Exception as e:
            self.logger.error(f"Error in sentiment analysis: {str(e)}")
            return 0.0

    @staticmethod
    def get_sentiment_label(score: float) -> str:
        """
        Convert a sentiment score to a label
        
        Args:
            score (float): Sentiment score between -1 and 1
            
        Returns:
            str: Sentiment label (Positive, Neutral, Negative)
        """
        if score > 0.2:
            return "Positive"
        elif score < -0.2:
            return "Negative"
        else:
            return "Neutral"