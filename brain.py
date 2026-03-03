import spacy
import wikipediaapi
from collections import Counter

nlp = spacy.load("en_core_web_sm")
wiki = wikipediaapi.Wikipedia("en")

TOPIC_KEYWORDS = {
    "Polity": ["constitution", "court", "parliament", "act", "bill", "election"],
    "Economy": ["gdp", "rbi", "inflation", "tax", "budget", "economy"],
    "Environment": ["climate", "biodiversity", "pollution", "forest", "wildlife"],
    "International Relations": ["united nations", "bilateral", "foreign", "treaty"],
    "Science & Tech": ["isro", "ai", "research", "technology", "innovation"],
    "Social Issues": ["education", "health", "poverty", "women", "child"]
}


def classify_article(text):
    doc = nlp(text.lower())
    word_list = [token.text for token in doc]

    scores = {}

    for topic, keywords in TOPIC_KEYWORDS.items():
        count = sum(word_list.count(k) for k in keywords)
        scores[topic] = count

    best_topic = max(scores, key=scores.get)

    if scores[best_topic] == 0:
        return None, 0

    return best_topic, scores[best_topic]


def extract_entities(text):
    doc = nlp(text)
    entities = list(set([ent.text for ent in doc.ents]))
    return entities[:5]


def enrich_entities(entities):
    enriched = []

    for entity in entities:
        page = wiki.page(entity)
        if page.exists():
            enriched.append(f"{entity}: {page.summary[:200]}")

    return enriched
