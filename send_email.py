import smtplib
from email.message import EmailMessage
import os

def send_email():

    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")
    email_to = os.getenv("EMAIL_TO")

    msg = EmailMessage()
    msg["Subject"] = "UPSC Daily Current Affairs"
    msg["From"] = email_user
    msg["To"] = email_to

    msg.set_content("Attached is today's UPSC current affairs report.")

    with open("upsc_daily_report.pdf", "rb") as f:
        file_data = f.read()

    msg.add_attachment(file_data,
                       maintype="application",
                       subtype="pdf",
                       filename="upsc_daily_report.pdf")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email_user, email_pass)
        smtp.send_message(msg)

    print("Email sent successfully")
