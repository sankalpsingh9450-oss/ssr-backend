from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.submissions import ContactSubmission
from app.schemas import ContactRequest, SuccessResponse
from app.services.email_service import send_email_notification, build_submission_email

router = APIRouter(prefix="/contact", tags=["Contact"])


@router.post("/", response_model=SuccessResponse)
async def submit_contact(
    data: ContactRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Handle contact form submissions."""
    submission = ContactSubmission(**data.model_dump())
    db.add(submission)
    await db.commit()
    await db.refresh(submission)

    # Send email notification in background
    email_html = build_submission_email("Contact Enquiry", {
        "name": data.name,
        "email": data.email,
        "phone": data.phone,
        "subject": data.subject,
        "message": data.message,
    })
    background_tasks.add_task(
        send_email_notification,
        subject=f"📩 New Contact: {data.subject} — {data.name}",
        body_html=email_html,
    )

    return SuccessResponse(
        message="Thank you for reaching out! We'll get back to you shortly.",
        data={"id": submission.id},
    )
