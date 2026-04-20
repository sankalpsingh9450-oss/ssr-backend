from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from app.database import Base
import enum


# ── Enums ──────────────────────────────────────────────

class PropertyType(str, enum.Enum):
    RESIDENTIAL_VILLA = "Residential — Villa"
    RESIDENTIAL_APARTMENT = "Residential — Apartment"
    RESIDENTIAL_INDEPENDENT = "Residential — Independent House"
    COMMERCIAL_OFFICE = "Commercial — Office Space"
    COMMERCIAL_RETAIL = "Commercial — Retail / Shop"
    INDUSTRIAL_WAREHOUSE = "Industrial — Warehouse"
    PLOT_LAND = "Plot / Land"


class ContactSubject(str, enum.Enum):
    PROPERTY_ENQUIRY = "Property Enquiry"
    CONSTRUCTION_QUOTE = "Construction Quote"
    BUILDING_MATERIALS = "Building Materials"
    PARTNERSHIP = "Partnership"
    OTHER = "Other"


class PartnerCategory(str, enum.Enum):
    MATERIAL_SUPPLIER = "Building Materials Supplier"
    SUB_CONTRACTOR = "Sub-Contractor"
    ARCHITECT = "Architect / Designer"
    EQUIPMENT_RENTAL = "Equipment Rental"
    LABOUR_CONTRACTOR = "Labour Contractor"
    OTHER = "Other"


class QuoteType(str, enum.Enum):
    FREE_QUOTATION = "Free Quotation"
    FULL_BOQ = "Full BOQ"


class ChatLeadSource(str, enum.Enum):
    CHATBOT = "chatbot"
    CALLBACK = "callback"


# ── Models ─────────────────────────────────────────────

class ContactSubmission(Base):
    __tablename__ = "contact_submissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    subject = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PropertyFinderSubmission(Base):
    __tablename__ = "property_finder_submissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    property_type = Column(String(50), nullable=False)
    budget_min = Column(String(50), nullable=True)
    budget_max = Column(String(50), nullable=True)
    preferred_location = Column(String(255), nullable=True)
    requirements = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class MaterialEnquiry(Base):
    __tablename__ = "material_enquiries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    material_type = Column(String(100), nullable=False)
    quantity = Column(String(100), nullable=True)
    delivery_location = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PartnerRegistration(Base):
    __tablename__ = "partner_registrations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    business_name = Column(String(200), nullable=False)
    contact_person = Column(String(150), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    category = Column(String(50), nullable=False)
    city = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class QuoteBOQRequest(Base):
    __tablename__ = "quote_boq_requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    request_type = Column(String(30), nullable=False)
    project_type = Column(String(100), nullable=True)
    plot_area = Column(String(100), nullable=True)
    location = Column(String(255), nullable=True)
    floors = Column(String(20), nullable=True)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ChatLeadSubmission(Base):
    __tablename__ = "chat_lead_submissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    service_interest = Column(String(120), nullable=False)
    source = Column(String(30), nullable=False, default=ChatLeadSource.CHATBOT.value)
    language = Column(String(10), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
