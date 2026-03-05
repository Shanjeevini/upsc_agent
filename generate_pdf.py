from fpdf import FPDF
from agent import agent_run
from datetime import datetime


def clean_text(text):
    return text.encode("latin-1", "replace").decode("latin-1")


def generate_pdf():

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, "UPSC Daily Current Affairs", ln=True, align="C")

    pdf.ln(5)

    pdf.set_font("Arial", "", 12)
    date = datetime.now().strftime("%d %B %Y")
    pdf.cell(0, 10, f"Date: {date}", ln=True, align="C")

    pdf.ln(10)

    notes = []

    try:

        notes = agent_run()

    except Exception as e:

        print("Agent error:", e)

    # if agent returned nothing
    if not notes:
        notes = ["No UPSC relevant news generated today."]

    topic_number = 1

    for note in notes:

        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"Topic {topic_number}", ln=True)

        pdf.set_font("Arial", "", 12)

        cleaned_note = clean_text(note)

        pdf.multi_cell(0, 8, cleaned_note)

        pdf.ln(5)

        topic_number += 1

    pdf.output("upsc_daily_report.pdf")

    print("PDF generated successfully")


if __name__ == "__main__":
    generate_pdf()
