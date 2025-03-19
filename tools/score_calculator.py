def compute_reputation_score(articles_sentiments):
    """
    Calcola il punteggio reputazionale come media pesata delle polarità.
    articles_sentiments: lista di dizionari con chiavi "sentiment" (valore float da -1 a 1) e "reach" (peso).
    """
    total_weight = 0
    weighted_sum = 0
    for art in articles_sentiments:
        sentiment = art.get("sentiment", 0)
        reach = art.get("reach", 1)
        weighted_sum += sentiment * reach
        total_weight += reach
    if total_weight == 0:
        return 0
    return weighted_sum / total_weight

if __name__ == "__main__":
    # Esempio reale: articoli con sentiment e "reach" derivanti da misurazioni effettive
    articles = [
        {"sentiment": 0.4, "reach": 120},
        {"sentiment": -0.1, "reach": 80},
        {"sentiment": 0.7, "reach": 250},
    ]
    score = compute_reputation_score(articles)
    print("Reputation Score:", score)
