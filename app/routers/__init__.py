from app.routers.contact import router as contact_router
from app.routers.property_finder import router as property_finder_router
from app.routers.materials import router as materials_router
from app.routers.partners import router as partners_router
from app.routers.quote import router as quote_router
from app.routers.admin import router as admin_router
from app.routers.chatbot import router as chatbot_router

__all__ = [
    "contact_router",
    "property_finder_router",
    "materials_router",
    "partners_router",
    "quote_router",
    "admin_router",
    "chatbot_router",
]
