import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from brain import classify_article, enrich_entities

RSS_FEEDS = [
    "https://www.thehindu.com/news/national/feeder/default.rss",
    "https://pib.gov.in/rssfeed.aspx"
]

def fetch_articles():
    today = datetime.now().date()
    articles = []

    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)

        for entry in feed.entries:
            try:
                published = datetime(*entry.published_parsed[:6]).date()
            except:
                continue

            if published == today:
                articles.append({
                    "title": entry.title,
                    "link": entry.link,
                })

    return articles


def extract_text(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        return " ".join([p.get_text() for p in paragraphs])
    except:
        return ""


def agent_run():
    print("🧠 Agent Activated")

    collected = fetch_articles()
    processed = []

    for article in collected:
        content = extract_text(article["link"])
        if len(content) < 300:
            continue

        topic, score = classify_article(content)

        if score < 0.30:
            continue  # reject low relevance

        enrichment = enrich_entities(article["title"])

        processed.append({
            "title": article["title"],
            "topic": topic,
            "score": score,
            "content": content[:800],
            "enrichment": enrichment
        })

    print(f"Selected {len(processed)} relevant articles.")
    return processed


if __name__ == "__main__":
    agent_run()