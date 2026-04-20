from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.submissions import ChatLeadSubmission
from app.schemas import ChatLeadRequest, ChatTranscriptRequest, SuccessResponse
from app.services.email_service import (
    send_email_notification,
    build_submission_email,
    build_transcript_email,
)
from app.services.hubspot_service import sync_hubspot_contact

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


@router.post("/lead", response_model=SuccessResponse)
async def submit_chatbot_lead(
    data: ChatLeadRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Store a chatbot-origin lead and trigger human follow-up notifications."""
    submission = ChatLeadSubmission(**data.model_dump())
    db.add(submission)
    await db.commit()
    await db.refresh(submission)

    email_html = build_submission_email("Chatbot Lead", {
        "name": data.name,
        "email": data.email,
        "phone": data.phone,
        "service_interest": data.service_interest,
        "source": data.source,
        "language": data.language,
        "notes": data.notes,
    })

    confirmation_html = build_submission_email("Chatbot Confirmation", {
        "hello": data.name,
        "message": f"Thank you for contacting SSR Group Civil. We have captured your interest in {data.service_interest} and our team will get in touch shortly.",
        "phone": data.phone,
        "service_interest": data.service_interest,
    })

    background_tasks.add_task(
        send_email_notification,
        subject=f"🤖 New Chat Lead: {data.service_interest} — {data.name}",
        body_html=email_html,
    )
    background_tasks.add_task(
        send_email_notification,
        subject="SSR Group Civil — We received your request",
        body_html=confirmation_html,
        to_email=data.email,
    )
    background_tasks.add_task(
        sync_hubspot_contact,
        email=data.email,
        phone=data.phone,
        full_name=data.name,
        lead_type="chatbot_lead",
        details={
            "service_interest": data.service_interest,
            "source": data.source,
            "language": data.language,
            "notes": data.notes,
        },
    )

    return SuccessResponse(
        message="Your chatbot enquiry has been captured successfully.",
        data={"id": submission.id},
    )


@router.post("/transcript", response_model=SuccessResponse)
async def send_chatbot_transcript(
    data: ChatTranscriptRequest,
    background_tasks: BackgroundTasks,
):
    """Email the chatbot transcript to the user and notify admin."""
    transcript_html = build_transcript_email(data.messages, data.email)

    background_tasks.add_task(
        send_email_notification,
        subject="SSR Group Civil — Your chatbot transcript",
        body_html=transcript_html,
        to_email=data.email,
    )
    background_tasks.add_task(
        send_email_notification,
        subject=f"💬 Chat Transcript Requested — {data.email}",
        body_html=transcript_html,
    )

    return SuccessResponse(
        message="Chat transcript email queued successfully.",
        data={"email": data.email, "messages": len(data.messages)},
    )
