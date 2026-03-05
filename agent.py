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

        try:
            print("Fetching:", feed_url)

            feed = feedparser.parse(feed_url)

            for entry in feed.entries[:5]:  # reduced headlines to save tokens
                if hasattr(entry, "title"):
                    headlines.append(entry.title)

        except Exception as e:
            print("RSS error:", e)

    print("Total headlines collected:", len(headlines))

    return headlines


# -----------------------------
# Main agent pipeline
# -----------------------------
def agent_run():

    print("Agent Activated")

    news_headlines = collect_news()

    if len(news_headlines) == 0:
        return ["No news could be fetched today."]

    final_notes = []

    for headline in news_headlines:

        if len(final_notes) >= 5:  # limit report size
            break

        try:

            print("Analyzing:", headline)

            analysis = evaluate_news(headline)

            if analysis is None:
                continue

            if analysis.get("relevant") != "Yes":
                continue

            category = analysis.get("category", "General")
            topic = analysis.get("topic", headline)

            print("Relevant:", category, "| Topic:", topic)

            background = retrieve_knowledge(topic)

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

        except Exception as e:

            print("Processing error:", e)
            continue

    if len(final_notes) == 0:
        final_notes.append(
            "UPSC relevant news could not be generated today."
        )

    print(f"\nGenerated notes for {len(final_notes)} important articles\n")

    return final_notes


if __name__ == "__main__":

    results = agent_run()

    for note in results:
        print(note)
