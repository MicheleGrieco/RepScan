import os

# General configurations
RSS_FEED_URL = "https://news.google.com/rss/search?q=Enel&hl=it&gl=IT&ceid=IT:it"
TARGET_COMPANY = "Enel"
ALERT_THRESHOLD = -0.3  # Alert threshold for sentiment score

# Email configurations
EMAIL_SENDER = os.environ.get("EMAIL_SENDER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EMAIL_RECIPIENT = os.environ.get("EMAIL_RECIPIENT", "admin@example.com")
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
DASHBOARD_TITLE = f"RepScan - Dashboard di Monitoraggio Reputazionale per {TARGET_COMPANY}"
DASHBOARD_REFRESH_RATE = 3600  # seconds (1 hour)