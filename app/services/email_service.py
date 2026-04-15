import aiosmtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


async def send_email_notification(
    subject: str,
    body_html: str,
    to_email: str = None,
):
    """Send an email notification to admin about a new form submission."""
    to_email = to_email or settings.ADMIN_EMAIL

    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        logger.warning("SMTP not configured — skipping email notification.")
        logger.info(f"[EMAIL WOULD SEND] To: {to_email} | Subject: {subject}")
        return False

    message = MIMEMultipart("alternative")
    message["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body_html, "html"))

    try:
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            start_tls=True,
        )
        logger.info(f"Email sent to {to_email}: {subject}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False


def build_submission_email(form_name: str, fields: dict) -> str:
    """Build a styled HTML email body for a form submission."""
    rows = ""
    for key, value in fields.items():
        label = key.replace("_", " ").title()
        rows += f"""
        <tr>
            <td style="padding:10px 14px;font-weight:600;color:#374151;
                        background:#f9fafb;border-bottom:1px solid #e5e7eb;
                        width:35%;vertical-align:top;">{label}</td>
            <td style="padding:10px 14px;color:#1f2937;
                        border-bottom:1px solid #e5e7eb;">{value or '—'}</td>
        </tr>"""

    return f"""
    <div style="font-family:'Segoe UI',Arial,sans-serif;max-width:600px;margin:0 auto;">
        <div style="background:linear-gradient(135deg,#1e3a5f,#2563eb);padding:24px 30px;
                     border-radius:8px 8px 0 0;">
            <h1 style="color:#fff;margin:0;font-size:20px;">🏗️ SSR Group</h1>
            <p style="color:#bfdbfe;margin:6px 0 0;font-size:14px;">
                New {form_name} Submission
            </p>
        </div>
        <div style="border:1px solid #e5e7eb;border-top:none;border-radius:0 0 8px 8px;
                     overflow:hidden;">
            <table style="width:100%;border-collapse:collapse;">{rows}</table>
        </div>
        <p style="text-align:center;color:#9ca3af;font-size:12px;margin-top:16px;">
            This is an automated notification from ssrgroupcivil.in
        </p>
    </div>
    """
