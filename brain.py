import os
import openai
import wikipediaapi

openai.api_key = os.getenv("OPENAI_API_KEY")

wiki = wikipediaapi.Wikipedia(
    user_agent="UPSC-AI-Agent",
    language="en"
)

def evaluate_news(headline):

    prompt = f"""
You are an expert UPSC and SSC exam analyst.

Evaluate the following news headline:

{headline}

Tasks:
1. Is this relevant for UPSC or SSC exams? (Yes or No)
2. If relevant, classify into one of these:
   World
   India
   Polity
   Economy
   Science & Technology
   Environment
   International Relations
   Tamil Nadu
3. Explain why it is important for competitive exams.
4. Extract the key topic entity (country, organization, person, institution).

Respond in JSON format.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.2
    )

    return response["choices"][0]["message"]["content"]


def retrieve_knowledge(topic):

    page = wiki.page(topic)

    if page.exists():

        text = page.summary[:1000]

        return text

    return ""


def generate_exam_notes(headline, topic, background):

    prompt = f"""
You are a UPSC current affairs analyst.

Headline:
{headline}

Topic:
{topic}

Background Knowledge:
{background}

Create exam ready notes.

Structure:

Summary
Key Facts
Important GK Points
Possible Exam Questions
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.3
    )

    return response["choices"][0]["message"]["content"]
