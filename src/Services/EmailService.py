import os
import smtplib
from email.message import EmailMessage


class EmailService:
    @staticmethod
    def send_pdf(to_email: str, subject: str, body: str, pdf_path: str):
        host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        port = int(os.getenv("SMTP_PORT", "587"))
        sender = os.getenv("SMTP_EMAIL")
        password = os.getenv("SMTP_PASSWORD")

        if not sender or not password:
            raise ValueError("Faltan SMTP_EMAIL o SMTP_PASSWORD en variables de entorno")

        message = EmailMessage()
        message["From"] = sender
        message["To"] = to_email
        message["Subject"] = subject
        message.set_content(body)

        with open(pdf_path, "rb") as pdf:
            message.add_attachment(
                pdf.read(),
                maintype="application",
                subtype="pdf",
                filename=os.path.basename(pdf_path),
            )

        with smtplib.SMTP(host, port) as smtp:
            smtp.starttls()
            smtp.login(sender, password)
            smtp.send_message(message)

    @staticmethod
    def send_invoice(to_email: str, subject: str, body: str, pdf_path: str):
        EmailService.send_pdf(to_email, subject, body, pdf_path)
