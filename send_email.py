import smtplib
import os
from email.message import EmailMessage

def send_email():

    EMAIL_USER = os.environ["EMAIL_USER"]
    EMAIL_PASS = os.environ["EMAIL_PASS"]
    EMAIL_TO = os.environ["EMAIL_TO"]

    msg = EmailMessage()
    msg["Subject"] = "UPSC Daily Current Affairs Report"
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO

    msg.set_content("Attached is today's UPSC Daily Current Affairs PDF report.")

    # attach PDF
    with open("upsc_daily_report.pdf", "rb") as f:
        file_data = f.read()

    msg.add_attachment(
        file_data,
        maintype="application",
        subtype="pdf",
        filename="upsc_daily_report.pdf"
    )

    print("Connecting to Gmail SMTP...")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)

    print("Sending email to:", EMAIL_TO)

if __name__ == "__main__":
    send_email()
