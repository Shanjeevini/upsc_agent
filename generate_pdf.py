from fpdf import FPDF
from datetime import datetime
from agent import agent_run
import traceback


# Fix for special characters that FPDF cannot handle
def clean_text(text):
    return text.encode("latin-1", "replace").decode("latin-1")


class UPSCPDF(FPDF):

    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "UPSC Daily Current Affairs", 0, 1, "C")

        today = datetime.now().strftime("%d %B %Y")
        self.set_font("Arial", "", 12)
        self.cell(0, 8, f"Date: {today}", 0, 1, "C")

        self.ln(10)


def generate_pdf():

    print("Starting UPSC Agent...")

    try:
        notes = agent_run()

        if not notes:
            print("Agent returned empty notes.")
            notes = ["No relevant news found today."]

    except Exception as e:

        print("Agent crashed! Printing full error:")
        traceback.print_exc()

        notes = ["Agent failed but PDF will still be created."]

    pdf = UPSCPDF()
    pdf.add_page()

    pdf.set_font("Arial", "", 12)

    for i, note in enumerate(notes, start=1):

        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, clean_text(f"Topic {i}"), 0, 1)

        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 8, clean_text(note))
        pdf.ln(5)

    filename = "upsc_daily_report.pdf"

    pdf.output(filename)

    print("PDF generated successfully:", filename)


if __name__ == "__main__":
    generate_pdf()
