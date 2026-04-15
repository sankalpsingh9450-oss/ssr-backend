from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.submissions import PropertyFinderSubmission
from app.schemas import PropertyFinderRequest, SuccessResponse
from app.services.email_service import send_email_notification, build_submission_email
from app.services.hubspot_service import sync_hubspot_contact

router = APIRouter(prefix="/property-finder", tags=["Property Finder"])


@router.post("/", response_model=SuccessResponse)
async def submit_property_request(
    data: PropertyFinderRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Handle property finder form submissions."""
    submission = PropertyFinderSubmission(**data.model_dump())
    db.add(submission)
    await db.commit()
    await db.refresh(submission)

    budget = ""
    if data.budget_min and data.budget_max:
        budget = f"₹{data.budget_min} — ₹{data.budget_max}"
    elif data.budget_min:
        budget = f"₹{data.budget_min}+"
    elif data.budget_max:
        budget = f"Up to ₹{data.budget_max}"

    email_html = build_submission_email("Property Finder", {
        "name": data.name,
        "email": data.email,
        "phone": data.phone,
        "property_type": data.property_type,
        "budget_range": budget,
        "preferred_location": data.preferred_location,
        "requirements": data.requirements,
    })
    background_tasks.add_task(
        send_email_notification,
        subject=f"🏠 Property Request: {data.property_type} — {data.name}",
        body_html=email_html,
    )
    background_tasks.add_task(
        sync_hubspot_contact,
        email=data.email,
        phone=data.phone,
        full_name=data.name,
        lead_type="property_finder",
        details={
            "property_type": data.property_type,
            "budget_min": data.budget_min,
            "budget_max": data.budget_max,
            "preferred_location": data.preferred_location,
            "requirements": data.requirements,
        },
    )

    return SuccessResponse(
        message="Sit back and relax! Our team will find the perfect property for you.",
        data={"id": submission.id},
    )
