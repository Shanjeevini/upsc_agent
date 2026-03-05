import feedparser
import json
from brain import evaluate_news, retrieve_knowledge, generate_exam_notes

RSS_FEEDS = [
    "https://www.thehindu.com/news/national/feeder/default.rss",
    "https://www.thehindu.com/news/international/feeder/default.rss"
]


def collect_news():

    articles = []

    for feed in RSS_FEEDS:

        parsed = feedparser.parse(feed)

        for entry in parsed.entries[:20]:

            articles.append(entry.title)

    return articles


def agent_run():

    print("🧠 Agent Activated")

    news = collect_news()

    final_notes = []

    for headline in news:

        print("Analyzing:", headline)

        analysis = evaluate_news(headline)

        try:

            data = json.loads(analysis)

        except:
            continue

        if data["relevant"] == "Yes":

            topic = data["topic"]

            background = retrieve_knowledge(topic)

            notes = generate_exam_notes(
                headline,
                topic,
                background
            )

            final_notes.append(notes)

    return final_notes
