from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


# ── Contact Form ───────────────────────────────────────

class ContactRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    subject: str = Field(..., max_length=50)
    message: str = Field(..., min_length=10, max_length=2000)


class ContactResponse(BaseModel):
    id: int
    name: str
    email: str
    subject: str
    created_at: datetime

    class Config:
        from_attributes = True


# ── Property Finder ────────────────────────────────────

class PropertyFinderRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    email: EmailStr
    phone: str = Field(..., max_length=20)
    property_type: str = Field(..., max_length=50)
    budget_min: Optional[str] = Field(None, max_length=50)
    budget_max: Optional[str] = Field(None, max_length=50)
    preferred_location: Optional[str] = Field(None, max_length=255)
    requirements: Optional[str] = Field(None, max_length=2000)


class PropertyFinderResponse(BaseModel):
    id: int
    name: str
    property_type: str
    created_at: datetime

    class Config:
        from_attributes = True


# ── Material Enquiry ───────────────────────────────────

class MaterialEnquiryRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    email: EmailStr
    phone: str = Field(..., max_length=20)
    material_type: str = Field(..., max_length=100)
    quantity: Optional[str] = Field(None, max_length=100)
    delivery_location: Optional[str] = Field(None, max_length=255)
    notes: Optional[str] = Field(None, max_length=2000)


class MaterialEnquiryResponse(BaseModel):
    id: int
    name: str
    material_type: str
    created_at: datetime

    class Config:
        from_attributes = True


# ── Partner Registration ──────────────────────────────

class PartnerRegistrationRequest(BaseModel):
    business_name: str = Field(..., min_length=2, max_length=200)
    contact_person: str = Field(..., min_length=2, max_length=150)
    email: EmailStr
    phone: str = Field(..., max_length=20)
    category: str = Field(..., max_length=50)
    city: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=2000)


class PartnerRegistrationResponse(BaseModel):
    id: int
    business_name: str
    category: str
    created_at: datetime

    class Config:
        from_attributes = True


# ── Quote / BOQ Request ───────────────────────────────

class QuoteBOQRequestSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    email: EmailStr
    phone: str = Field(..., max_length=20)
    request_type: str = Field(..., max_length=30)
    project_type: Optional[str] = Field(None, max_length=100)
    plot_area: Optional[str] = Field(None, max_length=100)
    location: Optional[str] = Field(None, max_length=255)
    floors: Optional[str] = Field(None, max_length=20)
    details: Optional[str] = Field(None, max_length=2000)


class QuoteBOQResponse(BaseModel):
    id: int
    name: str
    request_type: str
    created_at: datetime

    class Config:
        from_attributes = True


# ── Generic ───────────────────────────────────────────

class SuccessResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[dict] = None
