import feedparser

def fetch_articles(rss_url):
    """
    Scarica il feed RSS e restituisce una lista di articoli.
    Ogni articolo è un dizionario con titolo, link, data di pubblicazione e sommario.
    """
    feed = feedparser.parse(rss_url)
    articles = []
    for entry in feed.entries:
        article = {
            "title": entry.title,
            "link": entry.link,
            "published": entry.published,
            "summary": entry.summary
        }
        articles.append(article)
    return articles

if __name__ == "__main__":
    # Test: stampa i titoli degli articoli
    articles = fetch_articles("https://news.google.com/rss?hl=it&gl=IT&ceid=IT:it")
    for a in articles:
        print(a["title"])
