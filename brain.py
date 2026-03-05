import os
import json
from openai import OpenAI
import wikipediaapi

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Wikipedia setup
wiki = wikipediaapi.Wikipedia(
    user_agent="UPSC-AI-Agent",
    language="en"
)


# -----------------------------------
# 1️⃣ Evaluate news importance
# -----------------------------------

def evaluate_news(headline):

    prompt = f"""
You are an expert UPSC and SSC current affairs analyst.

Evaluate this news headline and determine if it is relevant for competitive exams.

Headline:
{headline}

Tasks:

1. Decide if this news is relevant for UPSC or SSC exams.
2. If relevant, classify it into one category:

World
India
Polity
Economy
Science & Technology
Environment
International Relations
Tamil Nadu

3. Extract the main topic/entity (country, organization, person, institution).

Respond ONLY in JSON format:

{{
"relevant": "Yes or No",
"category": "Category name",
"topic": "main topic/entity",
"reason": "Why this news matters for exams"
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    result = response.choices[0].message.content

    try:
        return json.loads(result)
    except:
        return None


# -----------------------------------
# 2️⃣ Retrieve background knowledge
# -----------------------------------

def retrieve_knowledge(topic):

    page = wiki.page(topic)

    if page.exists():
        return page.summary[:1200]

    return ""


# -----------------------------------
# 3️⃣ Generate UPSC exam notes
# -----------------------------------

def generate_exam_notes(headline, category, topic, background):

    prompt = f"""
You are a UPSC current affairs analyst.

Create exam-ready notes for the following news.

Headline:
{headline}

Category:
{category}

Main Topic:
{topic}

Background Knowledge:
{background}

Generate structured UPSC notes.

Format:

Summary

Key Points (bullet list)

Important GK Facts

Possible Exam Questions
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content
