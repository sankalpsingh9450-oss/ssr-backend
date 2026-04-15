from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.submissions import QuoteBOQRequest
from app.schemas import QuoteBOQRequestSchema, SuccessResponse
from app.services.email_service import send_email_notification, build_submission_email

router = APIRouter(prefix="/quote", tags=["Quote & BOQ"])


@router.post("/", response_model=SuccessResponse)
async def submit_quote_request(
    data: QuoteBOQRequestSchema,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Handle free quotation and BOQ request submissions."""
    submission = QuoteBOQRequest(**data.model_dump())
    db.add(submission)
    await db.commit()
    await db.refresh(submission)

    email_html = build_submission_email(f"{data.request_type} Request", {
        "name": data.name,
        "email": data.email,
        "phone": data.phone,
        "request_type": data.request_type,
        "project_type": data.project_type,
        "plot_area": data.plot_area,
        "location": data.location,
        "floors": data.floors,
        "details": data.details,
    })
    background_tasks.add_task(
        send_email_notification,
        subject=f"📋 {data.request_type}: {data.project_type or 'New'} — {data.name}",
        body_html=email_html,
    )

    return SuccessResponse(
        message=f"Your {data.request_type.lower()} request is in! We'll prepare it for you soon.",
        data={"id": submission.id},
    )
