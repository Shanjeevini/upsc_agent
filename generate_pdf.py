from fpdf import FPDF
from agent import agent_run
from datetime import datetime

def generate_pdf():
    articles = agent_run()

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, f"UPSC Current Affairs - {datetime.now().date()}", ln=True)

    for article in articles:
        pdf.ln(5)
        pdf.multi_cell(0, 8, f"Title: {article['title']}")
        pdf.multi_cell(0, 8, f"Category: {article['topic']}")
        pdf.multi_cell(0, 8, f"Key Points: {article['content']}")

        for enrich in article["enrichment"]:
            pdf.multi_cell(0, 8, f"Context: {enrich}")

        pdf.ln(5)

    filename = f"UPSC_{datetime.now().date()}.pdf"
    pdf.output(filename)

    print(f"PDF Generated: {filename}")


if __name__ == "__main__":
    generate_pdf()