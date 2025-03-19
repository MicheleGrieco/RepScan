import re
import nltk
from nltk.corpus import stopwords

# Scarica le stopword (se non già scaricate)
nltk.download('stopwords')

def clean_text(text):
    """
    Rimuove tag HTML, URL e caratteri non alfabetici,
    converte in minuscolo e normalizza gli spazi.
    """
    text = re.sub(r'<[^>]+>', '', text)       # Rimuove tag HTML
    text = re.sub(r'http\S+', '', text)         # Rimuove URL
    text = re.sub(r'[^a-zA-ZàèéìòùÀÈÉÌÒÙ\s]', '', text)  # Mantiene solo lettere e spazi
    text = text.lower()                        # Converti in minuscolo
    text = re.sub(r'\s+', ' ', text).strip()    # Rimuove spazi extra
    return text

def remove_stopwords(text, language='italian'):
    """
    Rimuove le stopword dal testo.
    """
    stop_words = set(stopwords.words(language))
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    return ' '.join(filtered_words)

if __name__ == "__main__":
    sample = "Questo è un esempio di testo! Visita https://example.com per maggiori informazioni."
    cleaned = clean_text(sample)
    no_stop = remove_stopwords(cleaned)
    print("Cleaned:", cleaned)
    print("Without stopwords:", no_stop)
