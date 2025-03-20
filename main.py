import logging
import os
import argparse
import pandas as pd
from datetime import datetime

from configuration.config import DATA_DIRECTORY, TARGET_COMPANY
from tools.scraper import collect_articles
from preprocessing.preprocess import preprocess_text
from tools.ner import is_company_mentioned, get_company_mentions
from tools.sentiment_analysis import analyze_sentiment, get_sentiment_label
from tools.score_calculator import calculate_reputation_score, save_reputation_score
from tools.alert import send_alert_email

# Configurazione del logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(DATA_DIRECTORY, "repscan.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_analysis():
    """
    Esegue l'intero flusso di analisi: raccolta articoli, preprocessing,
    riconoscimento delle entità, analisi del sentiment, calcolo del punteggio
    reputazionale e invio di alert se necessario.
    
    Returns:
        float: Punteggio reputazionale calcolato
    """
    # Assicurati che la directory dei dati esista
    os.makedirs(DATA_DIRECTORY, exist_ok=True)

    logger.info(f"=== Avvio analisi RepScan per {TARGET_COMPANY} ===")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Passo 1: Raccolta degli articoli
    logger.info("Passo 1: Raccolta degli articoli dal feed RSS")
    articles = collect_articles()
    logger.info(f"Raccolti {len(articles)} articoli")

    if not articles:
        logger.warning("Nessun articolo raccolto. L'analisi verrà interrotta.")
        return 0.0

    # Passo 2: Preprocessing e analisi per ogni articolo
    logger.info("Passo 2: Preprocessing e analisi degli articoli")
    relevant_articles = []

    for i, article in enumerate(articles):
        logger.info(f"Analisi dell'articolo {i+1}/{len(articles)}: {article['title']}")

        # Preprocessa il testo dell'articolo
        article['processed_content'] = preprocess_text(article['content'])
        article['processed_title'] = preprocess_text(article['title'])

        # Verifica se l'azienda target è menzionata
        article['mentions_company'] = is_company_mentioned(
            article['processed_title'] + " " + article['processed_content']
        )

        if article['mentions_company']:
            # Estrai le menzioni specifiche dell'azienda
            article['company_mentions'] = get_company_mentions(
                article['processed_content'], TARGET_COMPANY
            )

            # Analizza il sentiment
            article['sentiment_score'] = analyze_sentiment(article['processed_content'])
            article['sentiment_label'] = get_sentiment_label(article['sentiment_score'])

            logger.info(f"Articolo rilevante trovato: {article['title']} - Sentiment: {article['sentiment_score']:.2f}")
            relevant_articles.append(article)
        else:
            logger.info(f"Articolo non rilevante (non menziona {TARGET_COMPANY}): {article['title']}")

    logger.info(f"Trovati {len(relevant_articles)} articoli rilevanti che menzionano {TARGET_COMPANY}")

    # Passo 3: Calcola il punteggio reputazionale
    logger.info("Passo 3: Calcolo del punteggio reputazionale")
    if relevant_articles:
        reputation_score = calculate_reputation_score(relevant_articles)

        # Salva il punteggio
        save_reputation_score(reputation_score, timestamp)

        # Passo 4: Invia alert se necessario
        logger.info("Passo 4: Verifica della necessità di inviare alert")
        alert_sent = send_alert_email(reputation_score, relevant_articles)

        # Salva i risultati dettagliati per questa esecuzione
        save_detailed_results(relevant_articles, reputation_score, timestamp)

        logger.info(f"Analisi completata. Punteggio reputazionale: {reputation_score:.2f}")
        return reputation_score
    else:
        logger.warning(f"Nessun articolo rilevante trovato che menzioni {TARGET_COMPANY}")
        return 0.0

def save_detailed_results(articles, score, timestamp):
    """
    Salva i risultati dettagliati dell'analisi in un file CSV
    
    Args:
        articles (list): Lista di articoli analizzati
        score (float): Punteggio reputazionale
        timestamp (str): Timestamp dell'analisi
    """
    # Crea un DataFrame con i dettagli degli articoli
    results = []
    for article in articles:
        results.append({
            'timestamp': timestamp,
            'title': article['title'],
            'link': article['link'],
            'sentiment_score': article['sentiment_score'],
            'sentiment_label': article['sentiment_label'],
            'published': article.get('published', 'N/A')
        })

    if results:
        df = pd.DataFrame(results)

        # Crea il nome del file con timestamp
        filename = f"detailed_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(DATA_DIRECTORY, filename)

        # Salva i risultati
        df.to_csv(filepath, index=False)
        logger.info(f"Risultati dettagliati salvati in {filepath}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='RepScan - Monitoraggio Reputazione Aziendale')
    parser.add_argument('--dashboard', action='store_true', help='Avvia la dashboard Streamlit')

    args = parser.parse_args()

    if args.dashboard:
        logger.info("Avvio della dashboard Streamlit")
        # Importa la dashboard qui per evitare problemi di dipendenza circolare
        from view.dashboard import run_dashboard
        run_dashboard()
    else:
        # Esegui l'analisi
        run_analysis()