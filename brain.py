from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import wikipediaapi

model = SentenceTransformer("all-MiniLM-L6-v2")

# UPSC topic anchors (semantic goals)
TOPIC_DESCRIPTIONS = {
    "Polity": "Constitution Supreme Court Parliament governance judiciary fundamental rights",
    "Economy": "GDP inflation RBI fiscal policy IMF World Bank economy banking taxation",
    "Environment": "climate biodiversity conservation tiger reserve pollution UNFCCC",
    "International Relations": "bilateral relations UN NATO foreign policy diplomacy",
    "Science & Tech": "ISRO AI biotechnology research innovation technology",
    "Social Issues": "education health poverty women child development scheme"
}

topic_embeddings = {
    topic: model.encode(text) for topic, text in TOPIC_DESCRIPTIONS.items()
}

wiki = wikipediaapi.Wikipedia("en")

def classify_article(text):
    article_embedding = model.encode(text)
    scores = {}

    for topic, embedding in topic_embeddings.items():
        score = cosine_similarity(
            [article_embedding], [embedding]
        )[0][0]
        scores[topic] = score

    best_topic = max(scores, key=scores.get)
    return best_topic, scores[best_topic]


def enrich_entities(title):
    words = title.split()
    enriched = []

    for word in words:
        page = wiki.page(word)
        if page.exists():
            enriched.append(f"{word}: {page.summary[:300]}")

    return enriched