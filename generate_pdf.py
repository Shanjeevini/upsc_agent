from fpdf import FPDF
from datetime import datetime
from agent import agent_run


def clean_text(text):
    """
    Convert text to latin-1 compatible characters
    to avoid FPDF Unicode errors.
    """
    return text.encode("latin-1", "ignore").decode("latin-1")


def generate_pdf():

    print("📄 Generating UPSC Daily PDF...")

    # Run the agent to collect notes
    notes = agent_run()

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "UPSC Daily Current Affairs", ln=True, align="C")

    pdf.ln(5)

    # Date
    pdf.set_font("Arial", "", 12)
    date_str = datetime.now().strftime("%d %B %Y")
    pdf.cell(0, 10, f"Date: {date_str}", ln=True)

    pdf.ln(5)

    pdf.set_font("Arial", size=11)

    # Add each note
    for note in notes:

        safe_note = clean_text(note)

        pdf.multi_cell(0, 8, safe_note)
        pdf.ln(3)

    filename = "upsc_daily_notes.pdf"

    pdf.output(filename)

    print(f"✅ PDF Generated: {filename}")


if __name__ == "__main__":
    generate_pdf()
