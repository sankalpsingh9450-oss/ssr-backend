import logging
from typing import Any

import httpx

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def _split_name(full_name: str | None) -> tuple[str, str]:
    if not full_name:
        return "", ""
    parts = full_name.strip().split()
    if not parts:
        return "", ""
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], " ".join(parts[1:])


def _stringify_details(details: dict[str, Any]) -> str:
    lines = []
    for key, value in details.items():
        if value in (None, ""):
            continue
        label = key.replace("_", " ").title()
        lines.append(f"{label}: {value}")
    return "\n".join(lines)


def _build_contact_properties(
    *,
    email: str,
    phone: str | None = None,
    full_name: str | None = None,
    company: str | None = None,
    city: str | None = None,
    lead_type: str,
    details: dict[str, Any] | None = None,
) -> dict[str, str]:
    firstname, lastname = _split_name(full_name)
    properties: dict[str, str] = {
        "email": email,
        "lifecyclestage": settings.HUBSPOT_LIFECYCLE_STAGE,
        "hs_lead_status": settings.HUBSPOT_LEAD_STATUS,
    }
    if firstname:
        properties["firstname"] = firstname
    if lastname:
        properties["lastname"] = lastname
    if phone:
        properties["phone"] = phone
    if company:
        properties["company"] = company
    if city:
        properties["city"] = city
    if settings.HUBSPOT_FORM_TYPE_PROPERTY:
        properties[settings.HUBSPOT_FORM_TYPE_PROPERTY] = lead_type
    if settings.HUBSPOT_DETAILS_PROPERTY and details:
        properties[settings.HUBSPOT_DETAILS_PROPERTY] = _stringify_details(details)
    return properties


async def sync_hubspot_contact(
    *,
    email: str,
    phone: str | None = None,
    full_name: str | None = None,
    company: str | None = None,
    city: str | None = None,
    lead_type: str,
    details: dict[str, Any] | None = None,
) -> bool:
    if not settings.HUBSPOT_ACCESS_TOKEN:
        logger.info("HubSpot token not configured — skipping CRM sync.")
        return False

    properties = _build_contact_properties(
        email=email,
        phone=phone,
        full_name=full_name,
        company=company,
        city=city,
        lead_type=lead_type,
        details=details,
    )
    headers = {
        "Authorization": f"Bearer {settings.HUBSPOT_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {"properties": properties}
    update_url = f"{settings.HUBSPOT_BASE_URL}/crm/v3/objects/contacts/{email}"
    create_url = f"{settings.HUBSPOT_BASE_URL}/crm/v3/objects/contacts"

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.patch(
                update_url,
                params={"idProperty": "email"},
                headers=headers,
                json=payload,
            )
            if response.status_code == 404:
                response = await client.post(create_url, headers=headers, json=payload)
            response.raise_for_status()
        logger.info("Synced HubSpot contact for %s (%s)", email, lead_type)
        return True
    except Exception as exc:
        logger.exception("HubSpot sync failed for %s: %s", email, exc)
        return False
