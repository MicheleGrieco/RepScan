import logging
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from configuration.config import SENTIMENT_MODEL

logger = logging.getLogger(__name__)

# Usa un modello italiano disponibile
SENTIMENT_MODEL = "neuraly/bert-base-italian-cased-sentiment"

try:
    # Carica il modello e il tokenizer
    sentiment_analyzer = pipeline(
        "sentiment-analysis",
        model=SENTIMENT_MODEL,
        tokenizer=SENTIMENT_MODEL
    )
    logger.info(f"Modello di sentiment analysis {SENTIMENT_MODEL} caricato con successo")
except Exception as e:
    logger.error(f"Errore durante il caricamento del modello di sentiment: {str(e)}")
    # Fallback a un modello più semplice se necessario
    sentiment_analyzer = None

def analyze_sentiment(text):
    """
    Analizza il sentiment del testo utilizzando un modello preaddestrato

    Args:
        text (str): Testo da analizzare

    Returns:
        float: Punteggio di sentiment tra -1 (negativo) e 1 (positivo)
    """
    try:
        if sentiment_analyzer:
            # Limita il testo alla lunghezza massima accettata dal modello
            max_length = 512
            if len(text) > max_length:
                text = text[:max_length]

            result = sentiment_analyzer(text)

            # Converti il risultato in un punteggio tra -1 e 1
            # Assumendo che il modello restituisca etichette come POSITIVE/NEGATIVE/NEUTRAL
            if result[0]['label'] == 'POSITIVE':
                return result[0]['score']
            elif result[0]['label'] == 'NEGATIVE':
                return -result[0]['score']
            else:
                return 0.0
        else:
            # Implementazione di fallback semplice basata su parole chiave
            logger.warning("Usando analisi del sentiment di fallback basata su parole chiave")
            positive_words = ['ottimo', 'eccellente', 'positivo', 'buono', 'successo']
            negative_words = ['pessimo', 'negativo', 'cattivo', 'fallimento', 'problema']

            text = text.lower()
            positive_count = sum(1 for word in positive_words if word in text)
            negative_count = sum(1 for word in negative_words if word in text)

            total = positive_count + negative_count
            if total == 0:
                return 0.0

            return (positive_count - negative_count) / total

    except Exception as e:
        logger.error(f"Errore nell'analisi del sentiment: {str(e)}")
        return 0.0

def get_sentiment_label(score):
    """
    Converte un punteggio di sentiment in un'etichetta leggibile

    Args:
        score (float): Punteggio di sentiment tra -1 e 1

    Returns:
        str: Etichetta di sentiment (Positivo, Neutro, Negativo)
    """
    if score > 0.2:
        return "Positivo"
    elif score < -0.2:
        return "Negativo"
    else:
        return "Neutro"