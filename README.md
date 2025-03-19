# RepScan: Reputational Scanning Tool with Sentiment Analysis

RepScan è un tool per monitorare la reputazione aziendale attraverso la raccolta di dati da fonti online e l’analisi del sentiment. L’applicazione, sviluppata in Python, esegue le seguenti operazioni:

- **RSS Feed Scraper:** Scarica articoli da un feed RSS (ad esempio, Google News in italiano).
- **Preprocessing del Testo:** Pulisce e normalizza il testo rimuovendo tag HTML, URL, caratteri non alfabetici e stopword.
- **Named Entity Recognition (NER):** Utilizza spaCy per estrarre entità e verificare se l’azienda target (ad esempio “Apple”) viene menzionata.
- **Sentiment Analysis:** Impiega il pipeline di Hugging Face (transformers) per valutare la polarità del testo, mappando il rating su una scala da -1 (molto negativo) a +1 (molto positivo).
- **Calcolo del Punteggio Reputazionale:** Combina i risultati dei sentiment con eventuali pesi (ad es. "reach") per calcolare un indice medio.
- **Sistema di Alert:** Invia un’email di notifica se il punteggio reputazionale scende al di sotto di una soglia definita.
- **Dashboard Interattiva:** Fornisce una dashboard con Streamlit per visualizzare il trend del punteggio reputazionale nel tempo.

## Struttura del Progetto

- **config.py** – Contiene le configurazioni generali (URL del feed, impostazioni email, soglia di alert, ecc.).
- **scraper.py** – Modulo per il download degli articoli dal feed RSS.
- **preprocess.py** – Funzioni per la pulizia e normalizzazione del testo.
- **ner.py** – Modulo per il riconoscimento delle entità (NER) con spaCy.
- **sentiment_analysis.py** – Modulo per eseguire la sentiment analysis utilizzando Hugging Face.
- **score_calculator.py** – Funzione per il calcolo del punteggio reputazionale medio ponderato.
- **alert.py** – Modulo per l’invio degli alert via email.
- **dashboard.py** – Applicazione Streamlit per la visualizzazione dei trend.
- **main.py** – Script principale che coordina l’intero flusso (scraping, analisi, calcolo score e alert).
- **README.md** – Questo file.
- **requirements.txt** – Elenco delle librerie necessarie.

## Requisiti

- **Python 3.7+**
- **pip** (per l’installazione dei package)

## Installazione

1. **Clona il repository:**

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **(Opzionale) Crea e attiva un ambiente virtuale:**

   ```bash
   python -m venv venv
   source venv/bin/activate    # Su Windows: venv\Scripts\activate
   ```

3. **Installa i pacchetti richiesti:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Scarica il modello spaCy per l’italiano:**

   ```bash
   python -m spacy download it_core_news_sm
   ```

## Configurazione

Modifica il file `config.py` per impostare i seguenti parametri:

- **RSS_FEED_URL:** URL del feed RSS da monitorare.
- **Email Settings:** Configura EMAIL_SENDER, EMAIL_PASSWORD e EMAIL_RECEIVER.
- **SENTIMENT_THRESHOLD:** Valore soglia per l’invio degli alert.

## Utilizzo

1. **Esecuzione del Tool Principale:**

   Avvia lo script principale che esegue lo scraping, l’analisi del testo e il calcolo del punteggio reputazionale:

   ```bash
   python main.py
   ```

2. **Avvio della Dashboard:**

   Per visualizzare i trend del punteggio reputazionale tramite Streamlit:

   ```bash
   streamlit run dashboard.py
   ```

## Contributori

- **Michele Grieco** – m.grieco31@studenti.uniba.it

## License

Questo progetto è distribuito con [MIT License](LICENSE).

## Acknowledgements

- **Hugging Face transformers** per i modelli di sentiment analysis.
- **spaCy** per il riconoscimento delle entità.
- **Streamlit** per la creazione della dashboard interattiva.
