from transformers import pipeline

# Inizializza il pipeline per la sentiment analysis con un modello multilingue
sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

def analyze_sentiment(text):
    """
    Analizza il testo e restituisce una tuple (polarity, score).
    La polarity viene calcolata mappando il rating (1-5) in un valore da -1 a +1.
    """
    result = sentiment_pipeline(text)
    label = result[0]['label']   # Es. "4 stars"
    score = result[0]['score']
    rating = int(label.split()[0])  # Converte in intero
    polarity = (rating - 3) / 2.0   # Mappa: 1-> -1, 3-> 0, 5-> 1
    return polarity, score

if __name__ == "__main__":
    text = "Il prodotto di questa azienda è eccellente e il servizio clienti è ottimo!"
    polarity, score = analyze_sentiment(text)
    print("Polarity:", polarity, "Score:", score)
