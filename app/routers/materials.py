from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.submissions import MaterialEnquiry
from app.schemas import MaterialEnquiryRequest, SuccessResponse
from app.services.email_service import send_email_notification, build_submission_email
from app.services.hubspot_service import sync_hubspot_contact

router = APIRouter(prefix="/materials", tags=["Building Materials"])


@router.post("/", response_model=SuccessResponse)
async def submit_material_enquiry(
    data: MaterialEnquiryRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Handle building material enquiry submissions."""
    submission = MaterialEnquiry(**data.model_dump())
    db.add(submission)
    await db.commit()
    await db.refresh(submission)

    email_html = build_submission_email("Material Enquiry", {
        "name": data.name,
        "email": data.email,
        "phone": data.phone,
        "material_type": data.material_type,
        "quantity": data.quantity,
        "delivery_location": data.delivery_location,
        "notes": data.notes,
    })
    background_tasks.add_task(
        send_email_notification,
        subject=f"🧱 Material Enquiry: {data.material_type} — {data.name}",
        body_html=email_html,
    )
    background_tasks.add_task(
        sync_hubspot_contact,
        email=data.email,
        phone=data.phone,
        full_name=data.name,
        lead_type="materials",
        details={
            "material_type": data.material_type,
            "quantity": data.quantity,
            "delivery_location": data.delivery_location,
            "notes": data.notes,
        },
    )

    return SuccessResponse(
        message="Material enquiry received! We'll share the best prices shortly.",
        data={"id": submission.id},
    )
