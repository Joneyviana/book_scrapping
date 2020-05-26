import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config

subject = "Upload Book"
body = "This is an email with attachment sent from Python"
sender_email = config.sender_email
receiver_email = config.receiver_email
password = config.password

# Create a multipart message and set headers

def upload_email(filePath,file):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email

    message.attach(MIMEText(body, "plain"))

    with open(filePath, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
   
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        "attachment; filename="+file,
    )
    message.attach(part)
    text = message.as_string()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email,password)
        server.sendmail(sender_email, receiver_email, text)