import schedule
import time
from generate_pdf import generate_pdf

def job():
    print("⏰ Running 8PM job...")
    generate_pdf()

schedule.every().day.at("20:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)