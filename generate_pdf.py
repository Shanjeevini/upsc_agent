from fpdf import FPDF
from agent import agent_run
from datetime import datetime


def clean_text(text):
    """
    Remove unsupported unicode characters for FPDF
    """
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

    pdf.ln(15)

    try:

        notes = agent_run()

        if not notes:
            notes = ["No important UPSC news found today."]

    except Exception as e:

        print("Agent error:", e)

        notes = ["Agent encountered an error while collecting news."]

    # Write topics
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
