"""
Module name: score_calculator.py
Author: Michele Grieco
Description:
    This module provides a ReputationScoreCalculator class for calculating, saving, and retrieving reputation scores
    based on sentiment analysis of articles. It uses pandas for data handling and ensures the results are stored in a CSV file.
Usage:
    from tools.score_calculator import ReputationScoreCalculator
    calculator = ReputationScoreCalculator()
    score = calculator.calculate_reputation_score(articles)
    calculator.save_reputation_score(score)
    historical_scores = calculator.get_historical_scores()
"""

import pandas as pd # for data manipulation
import os
import logging 
from datetime import datetime
from configuration.config import DATA_DIRECTORY, RESULTS_FILE
from typing import Optional

class ReputationScoreCalculator:
    """
    Class for calculating, saving and retrieving reputation scores.
    """
    
    def __init__(self) -> None:
        """
        Initialize the ReputationScoreCalculator with logging configuration
        and ensure data directory exists.
        """
        # Logger configuration
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Create data directory if it doesn't exist
        os.makedirs(DATA_DIRECTORY, exist_ok=True)
        
        self.results_file = RESULTS_FILE

    def calculate_reputation_score(self, articles: list) -> float:
        """
        Calculate the reputation score based on the sentiment analysis of articles.
        
        Args:
            articles (list): List of dictionaries containing article data.
            
        Returns:
            float: Weighted average reputation score calculated from the articles.
        """
        if not articles:
            self.logger.warning("No articles provided for reputation score calculation.")
            return 0.0

        self.logger.info("Calculating reputation score from articles...")

        # Extract sentiment scores
        sentiment_scores = [article.get('sentiment_score', 0.0) for article in articles]

        # Calculate weights based on article length
        weights = [len(article.get('content', '')) for article in articles]

        # Normalize weights
        total_weight = sum(weights)
        if total_weight == 0:
            self.logger.warning("Total weight is zero, using equal weights for all articles.")
            weights = [1] * len(articles)
            total_weight = len(articles)

        normalized_weights = [w / total_weight for w in weights]

        # Calculate weighted average score
        weighted_score = sum(score * weight for score, weight 
                           in zip(sentiment_scores, normalized_weights))

        self.logger.info(f"Calculated reputation score: {weighted_score:.2f}")
        return weighted_score

    def save_reputation_score(self, score: float, timestamp: Optional[str] = None) -> None:
        """
        Save the reputation score to a CSV file.
        
        Args:
            score (float): Reputation score.
            timestamp (str, optional): Analysis timestamp. If None, uses current timestamp.
        """
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.logger.info(f"Saving reputation score: {score:.2f} at {timestamp}")

        # Create DataFrame for new record
        new_record = pd.DataFrame({
            'timestamp': [timestamp],
            'score': [score]
        })

        try:
            # Load existing file if present
            if os.path.exists(self.results_file):
                df = pd.read_csv(self.results_file)
                df = pd.concat([df, new_record], ignore_index=True)
            else:
                df = new_record

            # Save updated DataFrame
            df.to_csv(self.results_file, index=False)
            self.logger.info(f"Reputation score successfully saved to {self.results_file}")
        except Exception as e:
            self.logger.error(f"Error while saving reputation score: {e}")

    def get_historical_scores(self) -> pd.DataFrame:
        """
        Retrieve historical reputation scores from CSV file.
        
        Returns:
            pandas.DataFrame: DataFrame containing historical reputation scores.
        """
        if not os.path.exists(self.results_file):
            self.logger.warning(f"File {self.results_file} not found. Returning empty DataFrame.")
            return pd.DataFrame(columns=['timestamp', 'score'])

        try:
            df = pd.read_csv(self.results_file)
            self.logger.info(f"Loaded {len(df)} historical reputation score records")
            return df
        except Exception as e:
            self.logger.error(f"Error while loading reputation scores: {e}")
            return pd.DataFrame(columns=['timestamp', 'score'])