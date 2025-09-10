"""
Module name: config.py
Author: Michele Grieco
Description:
    This module contains configuration settings for the reputation monitoring application.
    It includes settings for RSS feed URLs, email configurations, sentiment analysis model,
    data storage paths, and dashboard settings.
Usage:
    Import this module to access configuration settings throughout the application.
"""

import os

# General configurations
RSS_FEED_URL = "https://news.google.com/rss/search?q=Enel&hl=it&gl=IT&ceid=IT:it"
TARGET_COMPANY = "Enel" # Target company for reputation monitoring
ALERT_THRESHOLD = -0.3  # Alert threshold for sentiment score

# Email configurations
EMAIL_SENDER = os.environ.get("EMAIL_SENDER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EMAIL_RECIPIENT = os.environ.get("EMAIL_RECIPIENT", "michelegrieco92@gmail.com")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Sentiment analysis configurations
SENTIMENT_MODEL = "dbmdz/bert-base-italian-uncased-sentiment"

# Data storage configurations
DATA_DIRECTORY = "data"
RESULTS_FILE = os.path.join(DATA_DIRECTORY, "reputation_scores.csv")

# SpaCy configurations
SPACY_MODEL = "it_core_news_sm"

# Dashboard configurations
DASHBOARD_TITLE = f"RepScan - Reputation Monitoring Dashboard for {TARGET_COMPANY}"
DASHBOARD_REFRESH_RATE = 3600  # seconds (1 hour)