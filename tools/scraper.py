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
    articles = fetch_articles("https://news.google.com/rss?hl=it&gl=IT&ceid=IT:it")
    print("Numero di articoli scaricati:", len(articles))
    for a in articles[:3]:
        print("-", a["title"])
