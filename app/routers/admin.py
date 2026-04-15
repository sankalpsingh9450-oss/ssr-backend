from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models.submissions import (
    ContactSubmission,
    PropertyFinderSubmission,
    MaterialEnquiry,
    PartnerRegistration,
    QuoteBOQRequest,
)
from app.config import get_settings

router = APIRouter(prefix="/admin", tags=["Admin"])
settings = get_settings()

# Simple API key auth for admin endpoints
ADMIN_API_KEY = settings.SECRET_KEY


def verify_admin(api_key: str = Query(..., alias="api_key")):
    if api_key != ADMIN_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return True


@router.get("/dashboard")
async def admin_dashboard(
    _: bool = Depends(verify_admin),
    db: AsyncSession = Depends(get_db),
):
    """Get a summary of all submissions."""
    counts = {}
    for label, model in [
        ("contacts", ContactSubmission),
        ("property_requests", PropertyFinderSubmission),
        ("material_enquiries", MaterialEnquiry),
        ("partner_registrations", PartnerRegistration),
        ("quote_requests", QuoteBOQRequest),
    ]:
        result = await db.execute(select(func.count(model.id)))
        counts[label] = result.scalar()

    counts["total"] = sum(counts.values())
    return {"success": True, "data": counts}


@router.get("/submissions/{form_type}")
async def get_submissions(
    form_type: str,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    _: bool = Depends(verify_admin),
    db: AsyncSession = Depends(get_db),
):
    """Get paginated submissions by form type."""
    model_map = {
        "contacts": ContactSubmission,
        "property": PropertyFinderSubmission,
        "materials": MaterialEnquiry,
        "partners": PartnerRegistration,
        "quotes": QuoteBOQRequest,
    }

    model = model_map.get(form_type)
    if not model:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid form type. Choose from: {', '.join(model_map.keys())}",
        )

    offset = (page - 1) * per_page

    # Total count
    count_result = await db.execute(select(func.count(model.id)))
    total = count_result.scalar()

    # Paginated results
    query = (
        select(model)
        .order_by(model.created_at.desc())
        .offset(offset)
        .limit(per_page)
    )
    result = await db.execute(query)
    items = result.scalars().all()

    return {
        "success": True,
        "data": {
            "items": [
                {c.name: getattr(item, c.name) for c in item.__table__.columns}
                for item in items
            ],
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": (total + per_page - 1) // per_page,
        },
    }
