import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import logging
import numpy as np
from configuration.config import SENTIMENT_MODEL

# Configurazione del logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Carica il modello e il tokenizer
try:
    tokenizer = AutoTokenizer.from_pretrained(SENTIMENT_MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(SENTIMENT_MODEL)
    logger.info(f"Modello di sentiment analysis {SENTIMENT_MODEL} caricato con successo")
except Exception as e:
    logger.error(f"Errore durante il caricamento del modello di sentiment: {e}")
    raise

def analyze_sentiment(text):
    """
    Analizza il sentiment del testo utilizzando un modello BERT
    
    Args:
        text (str): Testo da analizzare
        
    Returns:
        float: Punteggio di sentiment da -1 (molto negativo) a +1 (molto positivo)
    """
    if not text:
        return 0.0

    logger.info("Iniziata l'analisi del sentiment")

    try:
        # Tronca il testo se è troppo lungo per il modello
        max_length = tokenizer.model_max_length
        if len(text) > max_length:
            logger.warning(f"Testo troppo lungo ({len(text)} caratteri), verrà troncato a {max_length}")
            text = text[:max_length]

        # Tokenizza il testo
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

        # Inference
        with torch.no_grad():
            outputs = model(**inputs)

        # Ottieni i punteggi
        scores = outputs.logits.softmax(dim=1).detach().numpy()[0]

        # Mappa i punteggi sulla scala da -1 a +1
        # Assumi che il modello restituisca punteggi per [negativo, neutro, positivo]
        if len(scores) == 3:
            # Mappa [negativo, neutro, positivo] a [-1, 0, 1]
            sentiment_score = -1 * scores[0] + 0 * scores[1] + 1 * scores[2]
        elif len(scores) == 2:
            # Mappa [negativo, positivo] a [-1, 1]
            sentiment_score = -1 * scores[0] + 1 * scores[1]
        else:
            # Mappa punteggi più complessi
            # Normalizza in [-1, 1] con media ponderata
            weights = np.linspace(-1, 1, len(scores))
            sentiment_score = np.sum(weights * scores)

        logger.info(f"Sentiment analizzato: {sentiment_score:.2f}")
        return float(sentiment_score)
    except Exception as e:
        logger.error(f"Errore durante l'analisi del sentiment: {e}")
        return 0.0

def get_sentiment_label(score):
    """
    Converte un punteggio numerico in un'etichetta di sentiment
    
    Args:
        score (float): Punteggio di sentiment da -1 a +1
        
    Returns:
        str: Etichetta di sentiment (Molto Negativo, Negativo, Neutro, Positivo, Molto Positivo)
    """
    if score < -0.6:
        return "Molto Negativo"
    elif score < -0.2:
        return "Negativo"
    elif score < 0.2:
        return "Neutro"
    elif score < 0.6:
        return "Positivo"
    else:
        return "Molto Positivo"