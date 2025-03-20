import os

# Configurazioni generali
RSS_FEED_URL = "https://news.google.com/rss/search?q=Enel&hl=it&gl=IT&ceid=IT:it"
TARGET_COMPANY = "Enel"
ALERT_THRESHOLD = -0.3  # Soglia per inviare alert (sentiment negativo)

# Configurazioni email
EMAIL_SENDER = os.environ.get("EMAIL_SENDER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EMAIL_RECIPIENT = os.environ.get("EMAIL_RECIPIENT", "admin@example.com")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Configurazioni per la sentiment analysis
SENTIMENT_MODEL = "dbmdz/bert-base-italian-uncased-sentiment"

# Configurazioni per il salvataggio dei dati
DATA_DIRECTORY = "data"
RESULTS_FILE = os.path.join(DATA_DIRECTORY, "reputation_scores.csv")

# Configurazioni per SpaCy
SPACY_MODEL = "it_core_news_sm"

# Configurazioni per la dashboard
DASHBOARD_TITLE = f"RepScan - Dashboard di Monitoraggio Reputazionale per {TARGET_COMPANY}"
DASHBOARD_REFRESH_RATE = 3600  # in secondi (1 ora)