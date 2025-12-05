from fastapi import HTTPException
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiosmtplib
from dotenv import load_dotenv
from schemas import ContactMessage
from utils.logger import logger

load_dotenv()

async def send_email(contact: ContactMessage):
    """
    Send email using SMTP
    """
    # Get email configuration from environment variables
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    recipient_email = os.getenv("RECIPIENT_EMAIL", smtp_user)
    
    if not smtp_user or not smtp_password:
        raise HTTPException(
            status_code=500,
            detail="Email configuration is missing. Please set SMTP_USER and SMTP_PASSWORD."
        )
    
    # Create email message
    message = MIMEMultipart("alternative")
    message["Subject"] = f"Portfolio Contact: {contact.subject}"
    message["From"] = smtp_user
    message["To"] = recipient_email
    message["Reply-To"] = contact.email
    
    # Create email body
    text_content = f"""
    New Contact Form Submission
    
    Name: {contact.name}
    Email: {contact.email}
    Subject: {contact.subject}
    
    Message:
    {contact.message}
    """
    
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9; border-radius: 10px;">
                <h2 style="color: #4a5568; border-bottom: 2px solid #4299e1; padding-bottom: 10px;">
                    New Contact Form Submission
                </h2>
                <div style="background-color: white; padding: 20px; border-radius: 5px; margin-top: 20px;">
                    <p><strong>Name:</strong> {contact.name}</p>
                    <p><strong>Email:</strong> <a href="mailto:{contact.email}">{contact.email}</a></p>
                    <p><strong>Subject:</strong> {contact.subject}</p>
                    <hr style="border: 1px solid #e2e8f0; margin: 20px 0;">
                    <p><strong>Message:</strong></p>
                    <p style="white-space: pre-wrap;">{contact.message}</p>
                </div>
            </div>
        </body>
    </html>
    """
    
    part1 = MIMEText(text_content, "plain")
    part2 = MIMEText(html_content, "html")
    message.attach(part1)
    message.attach(part2)
    
    # Send email
    try:
        await aiosmtplib.send(
            message,
            hostname=smtp_host,
            port=smtp_port,
            username=smtp_user,
            password=smtp_password,
            start_tls=True,
        )
        logger.info("Email sent successfully.")
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send email: {str(e)}"
        )