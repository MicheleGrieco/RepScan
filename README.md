# RepScan - Corporate Reputation Monitoring

RepScan is an advanced system for monitoring corporate reputation that collects, analyzes, and evaluates online articles to determine public sentiment towards a target company. The system uses Natural Language Processing (NLP) and Machine Learning techniques to provide valuable insights into the company's perception in the media.

## Main Features

- **Automatic Article Collection**: Downloads articles from RSS feeds (e.g., Google News) related to the target company
- **Text Analysis**: Preprocessing, Named Entity Recognition, and Sentiment Analysis
- **Reputation Score Calculation**: Determines a quantitative index of corporate reputation
- **Alert System**: Automatic notifications when the score falls below a defined threshold
- **Interactive Dashboard**: Visualization of reputation trends over time

## System Architecture

The system is structured in independent modules that work together to provide a comprehensive analysis:

1. **Scraper**: Collects articles from configured RSS feeds
2. **Preprocessor**: Cleans and normalizes article text
3. **NER Engine**: Identifies mentions of the target company
4. **Sentiment Analyzer**: Evaluates text sentiment using Deep Learning models
5. **Score Calculator**: Calculates the reputation score by combining analysis results
6. **Alert System**: Sends notifications when necessary
7. **Dashboard**: Displays data interactively

## System Requirements

- Python 3.8+
- Internet connection for downloading articles and models
- RAM: at least 4GB (8GB recommended for better performance)
- Disk space: at least 2GB for NLP models

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/repscan.git
cd repscan
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download the Italian spaCy model:
```bash
python -m spacy download it_core_news_sm
```

4. Set environment variables (for the alert system):
```bash
# On Windows
setx EMAIL_SENDER "your_email@example.com"
setx EMAIL_PASSWORD "your_email_password"
setx EMAIL_RECIPIENT "recipient@example.com"
```

## Project Structure

```
repscan/
├── configuration/
│   └── config.py        # General configurations
├── preprocessing/
│   └── preprocess.py    # Text preprocessing module
├── tools/
│   ├── alert.py         # Alert system module
│   ├── ner.py          # Named Entity Recognition module
│   ├── scraper.py      # Article scraping module
│   ├── sentiment_analysis.py  # Sentiment analysis module
│   └── score_calculator.py    # Score calculation module
├── view/
│   └── dashboard.py     # Streamlit dashboard
├── main.py             # Main application script
├── data/               # Data directory
│   └── reputation_scores.csv  # Historical scores
└── requirements.txt    # Project dependencies
```

## Usage

### Run the analysis

```bash
python main.py
```

This command executes the RepScanAnalyzer which performs:
1. Article collection via RSS feeds
2. Text preprocessing and cleaning
3. Named Entity Recognition for company mentions
4. Sentiment analysis on relevant articles
5. Reputation score calculation
6. Alert sending if score is below threshold

### Start the dashboard

```bash
python main.py --dashboard
```

This command starts the Streamlit dashboard that displays reputation score trends over time.

## Configuration

Edit `configuration/config.py` to customize:
- `RSS_FEED_URL`: URL for article collection
- `TARGET_COMPANY`: Company name to monitor
- `ALERT_THRESHOLD`: Threshold for alerts
- `EMAIL_*`: Email configuration
- `SENTIMENT_MODEL`: Model for sentiment analysis
- `DATA_DIRECTORY`: Data storage location

## Automation

For Windows Task Scheduler:
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., every 6 hours)
4. Action: Start Program
5. Program/script: `python`
6. Arguments: `main.py`
7. Start in: `C:\path\to\repscan`

## Troubleshooting

### Article Collection Issues
- Check internet connection
- Verify RSS feed URL in config
- Check feed provider rate limits

### NLP Model Issues
Verify spaCy model installation:
```bash
python -m spacy download it_core_news_sm
```

### Alert System Issues
Check:
- Environment variables are set correctly
- SMTP server configuration
- Email permissions and security settings

## Contributors

- **Michele Grieco**

## Contact

For support or questions:
- Academic: [m.grieco31@studenti.uniba.it](mailto:m.grieco31@studenti.uniba.it)
- Personal: [michelegrieco92@gmail.com](mailto:michelegrieco92@gmail.com)
