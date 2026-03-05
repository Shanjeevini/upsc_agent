from fpdf import FPDF
from agent import agent_run


def clean_text(text):

    return text.replace("–","-").replace("’","'")


def generate_pdf():

    notes = agent_run()

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=12)

    pdf.cell(0,10,"UPSC DAILY CURRENT AFFAIRS",ln=True)

    for note in notes:

        note = clean_text(note)

        pdf.multi_cell(0,8,note)

        pdf.ln()

    pdf.output("upsc_daily_report.pdf")


if __name__ == "__main__":
    generate_pdf()
