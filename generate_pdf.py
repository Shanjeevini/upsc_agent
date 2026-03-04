from fpdf import FPDF
from agent import agent_run
from datetime import datetime


def clean_text(text):
    """
    Convert unicode characters to latin-1 safe text
    so FPDF will not crash.
    """
    return text.encode("latin-1", "replace").decode("latin-1")


def generate_pdf():

    print("🧠 Agent Activated")

    articles = agent_run()

    print(f"Selected {len(articles)} relevant articles.")

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, "UPSC Daily Current Affairs", ln=True)

    pdf.set_font("Arial", "", 12)
    today = datetime.now().strftime("%d %B %Y")
    pdf.cell(0, 10, f"Date: {today}", ln=True)

    pdf.ln(5)

    for article in articles:

        title = clean_text(article.get("title", ""))
        summary = clean_text(article.get("summary", ""))
        entities = article.get("entities", [])

        pdf.set_font("Arial", "B", 12)
        pdf.multi_cell(0, 8, title)

        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 6, summary)

        if entities:
            pdf.set_font("Arial", "I", 10)
            entity_text = "Related Topics: " + ", ".join(entities)
            entity_text = clean_text(entity_text)
            pdf.multi_cell(0, 6, entity_text)

        pdf.ln(4)

    filename = "upsc_daily_report.pdf"
    pdf.output(filename)

    print(f"PDF Generated: {filename}")


if __name__ == "__main__":
    generate_pdf()
