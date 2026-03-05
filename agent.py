import feedparser
from brain import evaluate_news, retrieve_knowledge, generate_exam_notes


# RSS feeds for news collection
RSS_FEEDS = [
    "https://www.thehindu.com/news/national/feeder/default.rss",
    "https://www.thehindu.com/news/international/feeder/default.rss",
    "https://www.thehindu.com/news/tamilnadu/feeder/default.rss"
]


# -----------------------------
# Collect news headlines
# -----------------------------
def collect_news():

    headlines = []

    for feed_url in RSS_FEEDS:

        feed = feedparser.parse(feed_url)

        for entry in feed.entries[:20]:
            headlines.append(entry.title)

    return headlines


# -----------------------------
# Main agent pipeline
# -----------------------------
def agent_run():

    print("🧠 Agent Activated")

    news_headlines = collect_news()

    print(f"Collected {len(news_headlines)} headlines")

    final_notes = []

    for headline in news_headlines:

        print("Analyzing:", headline)

        analysis = evaluate_news(headline)

        if analysis is None:
            continue

        # Skip non-relevant news
        if analysis["relevant"] != "Yes":
            continue

        category = analysis["category"]
        topic = analysis["topic"]

        print("Relevant:", category, "| Topic:", topic)

        # Retrieve background knowledge
        background = retrieve_knowledge(topic)

        # Generate UPSC notes
        notes = generate_exam_notes(
            headline,
            category,
            topic,
            background
        )

        formatted_note = f"""
====================================
Category: {category}

Headline:
{headline}

{notes}
====================================
"""

        final_notes.append(formatted_note)

    print(f"\nGenerated notes for {len(final_notes)} important articles\n")

    return final_notes


# Run agent if executed directly
if __name__ == "__main__":

    results = agent_run()

    for note in results:
        print(note)
