import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from configuration import config

def send_alert_email(subject, message):
    """
    Invia un'email di alert utilizzando le impostazioni reali definite in configuration.py.
    Le credenziali vengono prelevate dalle variabili d'ambiente.
    """
    sender_email = config.EMAIL_SENDER
    receiver_email = config.EMAIL_RECEIVER
    password = config.EMAIL_PASSWORD

    if password is None:
        print("Errore: la variabile d'ambiente REPSCAN_EMAIL_PASSWORD non è impostata.")
        return

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP(config.EMAIL_SMTP_SERVER, config.EMAIL_SMTP_PORT)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email inviata con successo!")
    except Exception as e:
        print("Errore nell'invio dell'email:", str(e))

if __name__ == "__main__":
    # Test reale: invia un alert
    send_alert_email("Alert RepScan: Test", "Questo è un messaggio di test per il sistema di alert di RepScan.")
