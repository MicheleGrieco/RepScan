import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from datetime import datetime
from configuration.config import (
    EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENT,
    SMTP_SERVER, SMTP_PORT, ALERT_THRESHOLD, TARGET_COMPANY
)

# Configurazione del logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def should_send_alert(score):
    """
    Determina se inviare un alert in base al punteggio reputazionale
    
    Args:
        score (float): Punteggio reputazionale
        
    Returns:
        bool: True se il punteggio è sotto la soglia di alert, False altrimenti
    """
    return score < ALERT_THRESHOLD

def create_alert_message(score, articles):
    """
    Crea il messaggio di alert con i dettagli degli articoli problematici
    
    Args:
        score (float): Punteggio reputazionale
        articles (list): Lista di dizionari contenenti gli articoli analizzati
        
    Returns:
        str: Messaggio di alert in formato HTML
    """
    # Formatta il punteggio
    score_str = f"{score:.2f}"

    # Ordina gli articoli per sentiment score (dal più negativo al più positivo)
    negative_articles = sorted(
        [a for a in articles if a.get('sentiment_score', 0) < 0],
        key=lambda x: x.get('sentiment_score', 0)
    )

    # Crea il messaggio HTML
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .alert {{ background-color: #f8d7da; padding: 15px; border-radius: 5px; }}
            .article {{ margin-bottom: 20px; padding: 10px; border-left: 4px solid #dc3545; }}
            .score {{ font-weight: bold; color: #dc3545; }}
            .title {{ font-weight: bold; }}
            .link {{ color: #0066cc; }}
        </style>
    </head>
    <body>
        <h2>⚠️ Alert - Punteggio Reputazionale Basso</h2>
        <div class="alert">
            <p>Il punteggio reputazionale per <strong>{TARGET_COMPANY}</strong> è attualmente <span class="score">{score_str}</span>, 
            che è al di sotto della soglia di alert ({ALERT_THRESHOLD}).</p>
            <p>Data e ora dell'analisi: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
        
        <h3>Articoli negativi rilevati:</h3>
    """

    # Aggiungi dettagli degli articoli negativi
    for article in negative_articles[:5]:  # Mostra solo i 5 articoli più negativi
        sentiment_score = article.get('sentiment_score', 0)
        sentiment_label = article.get('sentiment_label', 'N/A')
        title = article.get('title', 'Titolo non disponibile')
        link = article.get('link', '#')

        html += f"""
        <div class="article">
            <p class="title">{title}</p>
            <p>Sentiment: <span class="score">{sentiment_score:.2f}</span> ({sentiment_label})</p>
            <p><a href="{link}" class="link">Leggi l'articolo completo</a></p>
        </div>
        """

    html += """
        <p>Questo è un messaggio automatico generato dal sistema RepScan. Per favore, non rispondere a questa email.</p>
    </body>
    </html>
    """

    return html

def send_alert_email(score, articles):
    """
    Invia un'email di alert quando il punteggio reputazionale è troppo basso
    
    Args:
        score (float): Punteggio reputazionale
        articles (list): Lista di dizionari contenenti gli articoli analizzati
        
    Returns:
        bool: True se l'email è stata inviata con successo, False altrimenti
    """
    if not should_send_alert(score):
        logger.info("Punteggio reputazionale sopra la soglia di alert, nessun alert inviato")
        return False

    logger.info(f"Invio di un alert per punteggio reputazionale basso: {score:.2f}")

    # Verifica che le credenziali email siano impostate
    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        logger.error("Credenziali email non configurate. Impossibile inviare l'alert.")
        return False

    try:
        # Crea il messaggio
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"[ALERT] Punteggio Reputazionale Basso per {TARGET_COMPANY}: {score:.2f}"
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECIPIENT

        # Crea il corpo del messaggio
        html_content = create_alert_message(score, articles)
        msg.attach(MIMEText(html_content, 'html'))

        # Invia l'email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

        logger.info(f"Alert inviato con successo a {EMAIL_RECIPIENT}")
        return True
    except Exception as e:
        logger.error(f"Errore durante l'invio dell'alert: {e}")
        return False