from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.submissions import PartnerRegistration
from app.schemas import PartnerRegistrationRequest, SuccessResponse
from app.services.email_service import send_email_notification, build_submission_email

router = APIRouter(prefix="/partners", tags=["Partner Registration"])


@router.post("/", response_model=SuccessResponse)
async def register_partner(
    data: PartnerRegistrationRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Handle partner registration submissions."""
    submission = PartnerRegistration(**data.model_dump())
    db.add(submission)
    await db.commit()
    await db.refresh(submission)

    email_html = build_submission_email("Partner Registration", {
        "business_name": data.business_name,
        "contact_person": data.contact_person,
        "email": data.email,
        "phone": data.phone,
        "category": data.category,
        "city": data.city,
        "description": data.description,
    })
    background_tasks.add_task(
        send_email_notification,
        subject=f"🤝 New Partner: {data.business_name} ({data.category})",
        body_html=email_html,
    )

    return SuccessResponse(
        message="Welcome aboard! Your partner registration has been received.",
        data={"id": submission.id},
    )
