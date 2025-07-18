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
export EMAIL_SENDER=your_email@example.com
export EMAIL_PASSWORD=your_email_password
export EMAIL_RECIPIENT=recipient@example.com
```

## Configuration

The `config.py` file contains all the main system settings. Edit this file to customize:

- RSS feed URL
- Target company name
- Alert threshold
- Email settings
- Sentiment analysis model
- Data storage directory

## Usage

### Run the analysis

```bash
python main.py
```

This command runs the entire analysis process:
1. Article collection
2. Text preprocessing
3. Entity recognition
4. Sentiment analysis
5. Reputation score calculation
6. Alert sending (if necessary)

### Start the dashboard

```bash
python main.py --dashboard
```

This command starts the Streamlit dashboard that displays reputation score trends over time.

Alternatively, you can start the dashboard directly with:

```bash
streamlit run dashboard.py
```

## Automation

For continuous monitoring, it is recommended to set up a cron job to run the analysis periodically:

```bash
# Example cron job to run the analysis every 6 hours
0 */6 * * * cd /path/to/repscan && python main.py
```

## Project Structure

```
repscan/
├── config.py           # General configurations
├── scraper.py          # Article download module
├── preprocess.py       # Text cleaning functions
├── ner.py              # Entity recognition module
├── sentiment_analysis.py # Sentiment analysis module
├── score_calculator.py # Score calculation function
├── alert.py            # Alert sending module
├── dashboard.py        # Streamlit dashboard
├── main.py             # Main script
├── data/               # Data directory
│   └── reputation_scores.csv  # File with historical scores
└── requirements.txt    # Project dependencies
```

## Customization

### Adding New Sources

To add new article sources, edit the `config.py` file and update the RSS feed URL.

### Customizing the Sentiment Model

To use a different sentiment model, change the `SENTIMENT_MODEL` parameter in the `config.py` file.

### Adjusting the Alert Threshold

To modify the alert system sensitivity, adjust the `ALERT_THRESHOLD` parameter in the `config.py` file.

## Troubleshooting

### Issues downloading articles

If you encounter issues downloading articles, check:
- Internet connection
- Validity of the RSS feed URL
- Any rate limitations from the feed provider

### Errors with the spaCy model

If you encounter errors related to the spaCy model, make sure you have correctly downloaded the Italian model:
```bash
python -m spacy download it_core_news_sm
```

### Issues sending alerts

If alerts are not sent:
- Check that environment variables are set correctly
- Ensure the SMTP server is properly configured
- Make sure the application has the necessary permissions to send emails

## Contributors

- **Michele Grieco**

Contributions are welcome! If you want to contribute to the project:

1. Fork the repository
2. Create a branch for your feature (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Contacts

For questions or support, contact me at [m.grieco31@studenti.uniba.it](mailto:m.grieco31@studenti.uniba.it) / [michelegrieco92@gmail.com](mailto:michelegrieco92@gmail.com).
