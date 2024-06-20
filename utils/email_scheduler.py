from google.cloud import storage
from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, body, to):
    msg = MIMEMultipart()
    msg['From'] = 'you@example.com'
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.example.com', 587)
    server.starttls()
    server.login(msg['From'], 'yourpassword')
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()

def daily_job():
    # Import functions from file_processing and question_generation modules
    from utils.file_processing import extract_text_from_pdf, extract_text_from_docx
    from utils.question_generation import generate_questions

    storage_client = storage.Client()
    bucket = storage_client.bucket('your-gcloud-storage-bucket-name')

    files = File.query.all()
    combined_text = ""
    for file in files:
        blob = bucket.blob(file.filename)
        blob.download_to_filename(f'./uploads/{file.filename}')
        # Process file based on type
        if file.filename.endswith('.pdf'):
            combined_text += extract_text_from_pdf(f'./uploads/{file.filename}')
        elif file.filename.endswith('.docx'):
            combined_text += extract_text_from_docx(f'./uploads/{file.filename}')
        # Add more conditions for other file types...

    questions = generate_questions(combined_text)
    email_body = "\n\n".join([q['question'] for q in questions[:5]])
    send_email("Daily Quiz", email_body, "your-email@example.com")

scheduler = BackgroundScheduler()
scheduler.add_job(daily_job, 'interval', days=1)
