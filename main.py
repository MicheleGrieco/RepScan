"""
RepScan - Main analysis execution module.
Module name: main.py
Author: Michele Grieco
Description:
    This module contains the main execution logic for the RepScan reputation monitoring application.
    It orchestrates the workflow of collecting articles, preprocessing text, performing named entity recognition,
    conducting sentiment analysis, calculating reputation scores, and sending alerts if necessary.
    It also includes an option to launch a Streamlit dashboard for visualizing the results.
Usage:
    To run the analysis:
        python main.py
    To launch the Streamlit dashboard:
        python main.py --dashboard
    Ensure that all dependencies are installed and configured properly.
    The module uses various tools and configurations defined in other parts of the application.
"""

import logging
import os
import argparse
import pandas as pd
from datetime import datetime

from configuration.config import DATA_DIRECTORY, TARGET_COMPANY
from tools.scraper import ArticleScraper
from preprocessing.preprocess import TextPreprocessor
from tools.ner import NamedEntityRecognizer
from tools.sentiment_analysis import SentimentAnalyzer
from tools.score_calculator import ReputationScoreCalculator
from tools.alert import AlertSystem

class RepScanAnalyzer:
    """
    Main class for RepScan analysis execution.
    """
    
    def __init__(self):
        """
        Initialize RepScanAnalyzer with its configs and dependencies.
        """
        # Logging config
        self._setup_logging()
        self.scraper = ArticleScraper()
        self.preprocessor = TextPreprocessor()
        self.ner = NamedEntityRecognizer()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.score_calculator = ReputationScoreCalculator()
        self.alert_system = AlertSystem()
        
    def _setup_logging(self):
        """
        Setup logging configuration.
        """
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(DATA_DIRECTORY, "repscan.log")),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)


    def run_analysis(self) -> float:
        """
        Perform the entire analysis workflow: article collection, preprocessing,
        entity recognition, sentiment analysis, reputation scoring,
        and sending alerts if necessary.
        
        Returns:
            float: Reputational score calculated
        """
        # Assicurati che la directory dei dati esista
        # os.makedirs(DATA_DIRECTORY, exist_ok=True)

        self.logger.info(f"=== Starting RepScan analisys for {TARGET_COMPANY} ===")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Step 1: Collecting articles
        self.logger.info("Step 1: Articles collection from RSS feed")
        articles = self.scraper.collect_articles()
        if not articles:
            self.logger.warning("No article collected. The analysis will be stopped.")
            return 0.0
        
        # Step 2: Preprocessing and analysis
        self.logger.info("Step 2: Preprocessing and articles analysis")
        relevant_articles = self._process_articles(articles)
        
        # Step 3: Score calculation
        if not relevant_articles:
            self.logger.warning(f"No relevant articles found with {TARGET_COMPANY} mentions.")
            return 0.0
        
        return self._calculate_and_save_score(relevant_articles, timestamp)

    def _process_articles(self, articles: list) -> list:
        """
        Process the articles applying preprocessing, NER and sentiment analysis.
        Args:
            articles (list): List of articles to process.
        Returns:
            list: List of articles that mention the target company with sentiment scores.
        """
        relevant_articles = []
        
        for i, article in enumerate(articles):
            self.logger.info(f"Article {i+1}/{len(articles)} analysis: {article['title']}")
            
            # Preprocessing
            article['processed_content'] = self.preprocessor.preprocess(article['content'])
            article['processed_title'] = self.preprocessor.preprocess(article['title'])
            
            # Verify company mentions
            full_text = f"{article['processed_title']} {article['processed_content']}"
            if self.ner.is_company_mentioned(full_text):
                article['company_mentions'] = self.ner.get_company_mentions(
                    article['processed_content'], TARGET_COMPANY
                )
                
                # Sentiment analysis
                article['sentiment_score'] = self.sentiment_analyzer.analyze_sentiment(
                    article['processed_content']
                )
                article['sentiment_label'] = self.sentiment_analyzer.get_sentiment_label(
                    article['sentiment_score']
                )
                
                relevant_articles.append(article)
        return relevant_articles
            
    def _calculate_and_save_score(self, relevant_articles: list, timestamp: str) -> float:
        """
        Calculate, save score and handle alerts.
        Args:
            relevant_articles (list): List of relevant articles with sentiment scores.
            timestamp (str): Analysis timestamp.
        Returns:
            float: Reputational score calculated.
        """
        reputation_score = self.score_calculator.calculate_reputation_score(relevant_articles)
        self.score_calculator.save_reputation_score(reputation_score, timestamp)
        
        # Alert handling
        self.alert_system.send_alert_email(reputation_score, relevant_articles)
        
        # Save detailed results
        self._save_detailed_results(relevant_articles, reputation_score, timestamp)
        
        self.logger.info(f"Analysis completed. Reputational score: {reputation_score:.2f}")
        return reputation_score

    def _save_detailed_results(self, articles: list, score: float, timestamp: str) -> None:
        """
        Save analysis detailed results.
        Args:
            articles (list): List of analyzed articles.
            score (float): Reputational score.
            timestamp (str): Analysis timestamp.
        Returns:
            None
        """
        results = [{
            'timestamp': timestamp,
            'title': article['title'],
            'link': article['link'],
            'sentiment_score': article['sentiment_score'],
            'sentiment_label': article['sentiment_label'],
            'score': score,
            'published': article.get('published', 'N/A')
        } for article in articles]
        
        if results:
            df = pd.DataFrame(results)
            filename = f"detailed_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            filepath = os.path.join(DATA_DIRECTORY, filename)
            df.to_csv(filepath, index=False)
            self.logger.info(f"")
            
def main():
    """
    RepScan's entry point. Parses command line arguments to either run the analysis
    or launch the Streamlit dashboard.
    """
    parser = argparse.ArgumentParser(description='RepScan - Reputational Score Monitoring')
    parser.add_argument('--dashboard', action='store_true', help='Run Streamlit dashboard')
    args = parser.parse_args()
    
    if args.dashboard:
        from view.dashboard import run_dashboard
        run_dashboard()
    else:
        analyzer = RepScanAnalyzer()
        analyzer.run_analysis()
        
if __name__ == "__main__":
    main()