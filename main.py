import datetime
import config
from tools.scraper import fetch_articles
from preprocessing.preprocess import clean_text, remove_stopwords
from tools.ner import extract_entities
from tools.sentiment_analysis import analyze_sentiment
from tools.score_calculator import compute_reputation_score
from tools.alert import send_alert_email

def main():
    # Scarica gli articoli dal feed RSS reale
    articles = fetch_articles(config.RSS_FEED_URL)
    articles_sentiments = []

    for article in articles:
        # Combina titolo e sommario per ottenere contesto reale
        text = f"{article['title']}. {article['summary']}"
        cleaned_text = clean_text(text)
        cleaned_text = remove_stopwords(cleaned_text)

        # Estrai le entità per verificare se l'azienda target viene menzionata (caso reale)
        entities = extract_entities(cleaned_text)
        if not any(config.TARGET_COMPANY in ent[0].lower() for ent in entities):
            continue  # Considera solo gli articoli che menzionano il target

        # Analisi del sentiment su testo reale
        sentiment, score = analyze_sentiment(cleaned_text)

        # In una situazione reale, il "reach" potrebbe essere ricavato da metriche come il traffico della fonte;
        # qui utilizziamo il valore 1 per ogni articolo.
        articles_sentiments.append({
            "sentiment": sentiment,
            "reach": 1
        })

    if not articles_sentiments:
        print(f"Nessun articolo rilevante trovato che menzioni '{config.TARGET_COMPANY}'.")
        return

    # Calcola il punteggio reputazionale reale
    reputation_score = compute_reputation_score(articles_sentiments)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Timestamp: {timestamp}, Reputation Score: {reputation_score:.2f}")

    # Se il punteggio scende sotto la soglia reale, invia un alert via email
    if reputation_score < config.SENTIMENT_THRESHOLD:
        subject = "Alert RepScan: Basso punteggio reputazionale"
        message = f"Il punteggio reputazionale corrente è {reputation_score:.2f} (sotto la soglia {config.SENTIMENT_THRESHOLD}). Verifica immediatamente le fonti."
        send_alert_email(subject, message)

if __name__ == "__main__":
    main()

