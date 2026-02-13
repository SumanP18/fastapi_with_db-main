import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
load_dotenv()
sender_email = os.environ.get("SENDER_EMAIL", "")
app_password = os.environ.get("APP_PASSWORD", "")

# Create the email
def send_email(receiver_email: str, subject: str, content: str) -> None:
    """send an email to the receiver with the given subject and content"""
    msg = EmailMessage()
    msg.set_content(content)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    # Send the email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)

    print("Email sent!")

