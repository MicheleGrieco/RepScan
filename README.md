# RepScan - Monitoraggio Reputazione Aziendale

RepScan è un sistema avanzato per il monitoraggio della reputazione aziendale che raccoglie, analizza e valuta articoli online per determinare il sentiment pubblico verso un'azienda target. Il sistema utilizza tecniche di Natural Language Processing (NLP) e Machine Learning per fornire insight preziosi sulla percezione dell'azienda nei media.

## Funzionalità Principali

- **Raccolta Automatica di Articoli**: Scarica articoli da feed RSS (es. Google News) relativi all'azienda target
- **Analisi del Testo**: Preprocessing, Named Entity Recognition, e Sentiment Analysis
- **Calcolo del Punteggio Reputazionale**: Determina un indice quantitativo della reputazione aziendale
- **Sistema di Alert**: Notifiche automatiche quando il punteggio scende sotto una soglia definita
- **Dashboard Interattiva**: Visualizzazione dei trend reputazionali nel tempo

## Architettura del Sistema

Il sistema è strutturato in moduli indipendenti che lavorano insieme per fornire un'analisi completa:

1. **Scraper**: Raccoglie articoli da feed RSS configurati
2. **Preprocessor**: Pulisce e normalizza il testo degli articoli
3. **NER Engine**: Identifica menzioni dell'azienda target
4. **Sentiment Analyzer**: Valuta il sentiment del testo utilizzando modelli di Deep Learning
5. **Score Calculator**: Calcola il punteggio reputazionale combinando i risultati dell'analisi
6. **Alert System**: Invia notifiche quando necessario
7. **Dashboard**: Visualizza i dati in modo interattivo

## Requisiti di Sistema

- Python 3.8+
- Connessione internet per il download degli articoli e dei modelli
- Memoria RAM: almeno 4GB (8GB consigliati per migliori prestazioni)
- Spazio su disco: almeno 2GB per i modelli di NLP

## Installazione

1. Clone del repository:
```bash
git clone https://github.com/yourusername/repscan.git
cd repscan
```

2. Installazione delle dipendenze:
```bash
pip install -r requirements.txt
```

3. Download del modello italiano di spaCy:
```bash
python -m spacy download it_core_news_sm
```

4. Configurazione delle variabili d'ambiente (per il sistema di alert):
```bash
export EMAIL_SENDER=your_email@example.com
export EMAIL_PASSWORD=your_email_password
export EMAIL_RECIPIENT=recipient@example.com
```

## Configurazione

Il file `config.py` contiene tutte le impostazioni principali del sistema. Modifica questo file per personalizzare:

- URL del feed RSS
- Nome dell'azienda target
- Soglia per gli alert
- Impostazioni email
- Modello di sentiment analysis
- Directory per il salvataggio dei dati

## Utilizzo

### Esecuzione dell'analisi

```bash
python main.py
```

Questo comando esegue l'intero processo di analisi:
1. Raccolta degli articoli
2. Preprocessing del testo
3. Riconoscimento delle entità
4. Analisi del sentiment
5. Calcolo del punteggio reputazionale
6. Invio di alert (se necessario)

### Avvio della dashboard

```bash
python main.py --dashboard
```

Questo comando avvia la dashboard Streamlit che visualizza i trend del punteggio reputazionale nel tempo.

Alternativamente, puoi avviare direttamente la dashboard con:

```bash
streamlit run dashboard.py
```

## Automazione

Per un monitoraggio continuo, è consigliabile configurare un job cron per eseguire l'analisi periodicamente:

```bash
# Esempio di job cron per eseguire l'analisi ogni 6 ore
0 */6 * * * cd /path/to/repscan && python main.py
```

## Struttura del Progetto

```
repscan/
├── config.py           # Configurazioni generali
├── scraper.py          # Modulo per il download degli articoli
├── preprocess.py       # Funzioni per la pulizia del testo
├── ner.py              # Modulo per il riconoscimento delle entità
├── sentiment_analysis.py # Modulo per l'analisi del sentiment
├── score_calculator.py # Funzione per il calcolo del punteggio
├── alert.py            # Modulo per l'invio degli alert
├── dashboard.py        # Dashboard Streamlit
├── main.py             # Script principale
├── data/               # Directory per i dati
│   └── reputation_scores.csv  # File con i punteggi storici
└── requirements.txt    # Dipendenze del progetto
```

## Customizzazione

### Aggiunta di Nuove Fonti

Per aggiungere nuove fonti di articoli, modifica il file `config.py` e aggiorna l'URL del feed RSS.

### Personalizzazione del Modello di Sentiment

Per utilizzare un modello di sentiment diverso, modifica il parametro `SENTIMENT_MODEL` nel file `config.py`.

### Regolazione della Soglia di Alert

Per modificare la sensibilità del sistema di alert, regola il parametro `ALERT_THRESHOLD` nel file `config.py`.

## Troubleshooting

### Problemi con il download degli articoli

Se riscontri problemi con il download degli articoli, verifica:
- La connessione internet
- La validità dell'URL del feed RSS
- Eventuali limitazioni di rate dal provider del feed

### Errori con il modello di spaCy

Se incontri errori relativi al modello di spaCy, assicurati di aver scaricato correttamente il modello italiano:
```bash
python -m spacy download it_core_news_sm
```

### Problemi con l'invio degli alert

Se gli alert non vengono inviati:
- Verifica che le variabili d'ambiente siano impostate correttamente
- Assicurati che il server SMTP sia configurato correttamente
- Controlla che l'applicazione abbia le autorizzazioni necessarie per inviare email

## Contributori

- **Michele Grieco**

Sono aperto a contributi! Se desideri contribuire al progetto:

1. Fai un fork del repository
2. Crea un branch per la tua feature (`git checkout -b feature/amazing-feature`)
3. Commit dei tuoi cambiamenti (`git commit -m 'Add some amazing feature'`)
4. Push al branch (`git push origin feature/amazing-feature`)
5. Apri una Pull Request

## Contatti

Per domande o supporto, contattami a [m.grieco31@studenti.uniba.it](mailto:m.grieco31@studenti.uniba.itm) / [michelegrieco92@gmail.com](mailto:michelegrieco92@gmail.com).
