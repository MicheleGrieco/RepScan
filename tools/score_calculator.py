import pandas as pd
import os
import logging
from datetime import datetime
from configuration.config import DATA_DIRECTORY, RESULTS_FILE

# Configurazione del logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Crea la directory dei dati se non esiste
os.makedirs(DATA_DIRECTORY, exist_ok=True)

def calculate_reputation_score(articles):
    """
    Calcola il punteggio reputazionale medio ponderato
    
    Args:
        articles (list): Lista di dizionari contenenti gli articoli analizzati
        
    Returns:
        float: Punteggio reputazionale medio
    """
    if not articles:
        logger.warning("Nessun articolo disponibile per il calcolo del punteggio reputazionale")
        return 0.0

    logger.info("Calcolo del punteggio reputazionale")

    # Estrai i sentiment scores e i pesi
    sentiment_scores = [article.get('sentiment_score', 0.0) for article in articles]

    # Calcola i pesi in base alla lunghezza del contenuto dell'articolo
    # Articoli più lunghi hanno un peso maggiore (ipotesi: più contenuto = più rilevante)
    weights = [len(article.get('content', '')) for article in articles]

    # Normalizza i pesi
    total_weight = sum(weights)
    if total_weight == 0:
        logger.warning("Peso totale zero, utilizzo pesi uniformi")
        weights = [1] * len(articles)
        total_weight = len(articles)

    normalized_weights = [w / total_weight for w in weights]

    # Calcola il punteggio medio ponderato
    weighted_score = sum(score * weight for score, weight in zip(sentiment_scores, normalized_weights))

    logger.info(f"Punteggio reputazionale calcolato: {weighted_score:.2f}")
    return weighted_score

def save_reputation_score(score, timestamp=None):
    """
    Salva il punteggio reputazionale in un file CSV
    
    Args:
        score (float): Punteggio reputazionale
        timestamp (str, optional): Timestamp dell'analisi. Se None, usa il timestamp corrente.
    """
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    logger.info(f"Salvataggio del punteggio reputazionale: {score:.2f} al {timestamp}")

    # Crea un DataFrame per il nuovo record
    new_record = pd.DataFrame({
        'timestamp': [timestamp],
        'score': [score]
    })

    try:
        # Carica il file esistente se presente
        if os.path.exists(RESULTS_FILE):
            df = pd.read_csv(RESULTS_FILE)
            df = pd.concat([df, new_record], ignore_index=True)
        else:
            df = new_record

        # Salva il DataFrame aggiornato
        df.to_csv(RESULTS_FILE, index=False)
        logger.info(f"Punteggio reputazionale salvato con successo in {RESULTS_FILE}")
    except Exception as e:
        logger.error(f"Errore durante il salvataggio del punteggio reputazionale: {e}")

def get_historical_scores():
    """
    Recupera i punteggi reputazionali storici dal file CSV
    
    Returns:
        pandas.DataFrame: DataFrame contenente i punteggi reputazionali storici
    """
    if not os.path.exists(RESULTS_FILE):
        logger.warning(f"File {RESULTS_FILE} non trovato. Restituisco un DataFrame vuoto.")
        return pd.DataFrame(columns=['timestamp', 'score'])

    try:
        df = pd.read_csv(RESULTS_FILE)
        logger.info(f"Caricati {len(df)} record di punteggi reputazionali storici")
        return df
    except Exception as e:
        logger.error(f"Errore durante il caricamento dei punteggi reputazionali: {e}")
        return pd.DataFrame(columns=['timestamp', 'score'])