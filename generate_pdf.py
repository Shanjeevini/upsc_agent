from fpdf import FPDF
from datetime import datetime
from agent import agent_run


# Fix for Unicode characters that FPDF cannot encode
def clean_text(text):
    return text.encode("latin-1", "replace").decode("latin-1")


class UPSCPDF(FPDF):

    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "UPSC Daily Current Affairs", 0, 1, "C")

        today = datetime.now().strftime("%d %B %Y")
        self.set_font("Arial", "", 12)
        self.cell(0, 8, f"Date: {today}", 0, 1, "C")

        self.ln(5)

    def section_title(self, title):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, clean_text(title), 0, 1)

    def section_body(self, text):
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 8, clean_text(text))
        self.ln(3)


def generate_pdf():

    print("Running UPSC Agent...")

    try:
        notes = agent_run()
   except Exception as e:
    import traceback
    print("Agent error:")
    traceback.print_exc()
    notes = ["Agent failed but PDF will still be created."]

    pdf = UPSCPDF()
    pdf.add_page()

    for i, note in enumerate(notes, 1):
        pdf.section_title(f"Topic {i}")
        pdf.section_body(note)

    filename = "upsc_daily_report.pdf"

    pdf.output(filename)

    print("PDF generated successfully:", filename)


if __name__ == "__main__":
    generate_pdf()

