# config.py

# URL del feed RSS (in questo esempio, il feed di Google News in italiano)
RSS_FEED_URL = "https://news.google.com/rss?hl=it&gl=IT&ceid=IT:it"

# Impostazioni per l'invio degli alert via email
EMAIL_SMTP_SERVER = "smtp.gmail.com"
EMAIL_SMTP_PORT = 587
EMAIL_SENDER = "michelegrieco@gmail.com"
EMAIL_PASSWORD = "your_email_password"
EMAIL_RECEIVER = "receiver_email@gmail.com"

# Soglia di alert: se il punteggio reputazionale (calcolato come media dei sentiment) scende sotto questo valore, invia un alert
SENTIMENT_THRESHOLD = -0.5
