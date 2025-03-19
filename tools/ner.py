import spacy

# Carica il modello italiano (se non lo hai già, installalo con: python -m spacy download it_core_news_sm)
nlp = spacy.load("it_core_news_sm")

def extract_entities(text):
    """
    Estrae le entità dal testo e restituisce una lista di tuple (entità, etichetta).
    """
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

if __name__ == "__main__":
    text = "Apple Inc. ha sede a Cupertino, California. L'azienda è stata fondata da Steve Jobs."
    ents = extract_entities(text)
    print(ents)
