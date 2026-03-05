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
You are an expert UPSC and SSC exam analyst.

Evaluate the following news headline.

Headline:
{headline}

Tasks:

1. Determine if this news is relevant for competitive exams.
2. If relevant, classify into one category:

World
India
Polity
Economy
Science & Technology
Environment
International Relations
Tamil Nadu

3. Extract the main topic/entity.

Respond ONLY in JSON format:

{{
"relevant": "Yes or No",
"category": "category name",
"topic": "main entity",
"reason": "why it matters for exams"
}}
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
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
You are a UPSC current affairs expert.

Create exam-ready notes for the following news.

Headline:
{headline}

Category:
{category}

Topic:
{topic}

Background Knowledge:
{background}

Generate structured notes.

Format:

Summary

Key Points

Important GK Facts

Possible Exam Questions
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
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
Could not generate detailed notes due to API error.

Important GK Facts:
Topic: {topic}

Possible Exam Questions:
What is the significance of {topic}?
"""
