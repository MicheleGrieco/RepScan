from transformers import pipeline

# Inizializza il pipeline per la sentiment analysis con un modello multilingue reale.
# Il modello "nlptown/bert-base-multilingual-uncased-sentiment" è addestrato su recensioni in diverse lingue.
sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

def analyze_sentiment(text):
    """
    Analizza il testo e restituisce una tuple (polarity, score).
    La polarity viene calcolata mappando il rating (1-5) in un valore da -1 a +1.
    """
    result = sentiment_pipeline(text)
    label = result[0]['label']   # ad es. "4 stars"
    score = result[0]['score']
    rating = int(label.split()[0])
    polarity = (rating - 3) / 2.0   # Mappa: 1-> -1, 3-> 0, 5-> 1
    return polarity, score

if __name__ == "__main__":
    positive_text = "La qualità dei prodotti di Enel è eccellente e il servizio clienti è molto apprezzato."
    negative_text = "L'efficienza della gestione è scarsa e i problemi tecnici si ripetono frequentemente."
    polarity_pos, score_pos = analyze_sentiment(positive_text)
    polarity_neg, score_neg = analyze_sentiment(negative_text)

    print("Testo positivo:")
    print(positive_text)
    print(f"Polarity: {polarity_pos:.2f}, Score: {score_pos:.2f}\n")

    print("Testo negativo:")
    print(negative_text)
    print(f"Polarity: {polarity_neg:.2f}, Score: {score_neg:.2f}")
