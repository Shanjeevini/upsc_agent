import os
import json
import re
from groq import Groq
import wikipediaapi


# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# Wikipedia setup
wiki = wikipediaapi.Wikipedia(
    user_agent="UPSC-AI-Agent",
    language="en"
)


# ------------------------------
# Extract JSON safely
# ------------------------------
def extract_json(text):

    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass

    return None


# ------------------------------
# Evaluate if news is important
# ------------------------------
def evaluate_news(headline):

    prompt = f"""
You are a UPSC exam analyst.

Evaluate this headline.

Headline:
{headline}

Tasks:
1. Is it relevant for competitive exams?
2. Classify category.

Categories:
World
India
Polity
Economy
Science & Technology
Environment
International Relations
Tamil Nadu

Return JSON only:

{{
"relevant":"Yes or No",
"category":"category",
"topic":"main entity"
}}
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a UPSC current affairs expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        result = response.choices[0].message.content

        parsed = extract_json(result)

        return parsed

    except Exception as e:

        print("LLM evaluation error:", e)

        return None


# ------------------------------
# Retrieve background knowledge
# ------------------------------
def retrieve_knowledge(topic):

    try:

        if topic is None:
            return ""

        page = wiki.page(topic)

        if page.exists():
            return page.summary[:1200]

    except Exception as e:

        print("Wikipedia error:", e)

    return ""


# ------------------------------
# Generate exam notes
# ------------------------------
def generate_exam_notes(headline, category, topic, background):

    prompt = f"""
Create UPSC exam notes.

Headline:
{headline}

Category:
{category}

Topic:
{topic}

Background:
{background}

Format:

Summary
Key Points
Important Facts
Possible Questions
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        return response.choices[0].message.content

    except Exception as e:

        print("Note generation error:", e)

        return f"""
Summary:
{headline}

Key Points:
Unable to generate full notes.

Topic:
{topic}
"""
