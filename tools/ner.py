import spacy

# Carica il modello italiano (assicurarsi di averlo installato con: python -m spacy download it_core_news_sm)
nlp = spacy.load("it_core_news_sm")

def extract_entities(text):
    """
    Estrae le entità dal testo e restituisce una lista di tuple (entità, etichetta).
    """
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

if __name__ == "__main__":
    text = "Enel è una delle maggiori aziende energetiche italiane, con sede a Roma e operante in molti paesi."
    ents = extract_entities(text)
    print("Entità estratte:")
    for ent, label in ents:
        print(f"{ent} -> {label}")
