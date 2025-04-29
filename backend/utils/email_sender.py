import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

GMAIL_EMAIL = os.getenv("GMAIL_EMAIL")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def send_verification_email(to_email: str, verification_link: str):
    """
    Send an email using Gmail SMTP with a verification link.
    """
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Verify your email address"
    msg["From"] = GMAIL_EMAIL
    msg["To"] = to_email

    html_content = f"""
    <html>
      <body>
        <p>Click this link to verify your email: <a href="{verification_link}">{verification_link}</a></p>
      </body>
    </html>
    """
    part = MIMEText(html_content, "html")
    msg.attach(part)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(GMAIL_EMAIL, GMAIL_PASSWORD)
            server.sendmail(GMAIL_EMAIL, to_email, msg.as_string())
    except Exception as e:
        raise Exception(f"Failed to send email: {e}")
