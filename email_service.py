import smtplib
import os
from email.message import EmailMessage

# Load email credentials from environment variables (recommended for security)
EMAIL_ADDRESS = "tejuselvaraj2006@gmail.com"  # Replace with your email
EMAIL_PASSWORD = "tyrw nkfd rihr tydh"  # Use App Password (not your real password)

# Function to send email
def send_email(to_email, subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"📧 Email sent successfully to {to_email}")
    except Exception as e:
        print(f"⚠ Error sending email: {e}")

# Test Email Sending (Run this file directly to test)
if __name__ == "__main__":
    send_email("test@example.com", "Test Email", "This is a test email from ResumeScreen AI.")
