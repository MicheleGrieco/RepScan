import os

# URL del feed RSS di Google News in italiano (reale)
RSS_FEED_URL = "https://news.google.com/rss?hl=it&gl=IT&ceid=IT:it"

# Impostazioni per l'invio degli alert via email.
# Le credenziali vengono lette da variabili d'ambiente per evitare di inserirle in chiaro.
EMAIL_SMTP_SERVER = "smtp.gmail.com"
EMAIL_SMTP_PORT = 587
EMAIL_SENDER = os.environ.get("REPSCAN_EMAIL_SENDER", "m.grieco31@studenti.uniba.it")
EMAIL_PASSWORD = os.environ.get("REPSCAN_EMAIL_PASSWORD")  # Assicurarsi di impostare questa variabile
EMAIL_RECEIVER = "m.grieco31@studenti.uniba.it"  # Email reale di ricezione

# Soglia per l'invio degli alert: se il punteggio reputazionale (media dei sentiment) scende sotto questo valore, viene inviato un alert
SENTIMENT_THRESHOLD = -0.3

# Azienda target (reale) da monitorare nei testi
TARGET_COMPANY = "enel"