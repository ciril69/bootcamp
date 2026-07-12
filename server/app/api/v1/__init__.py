from fastapi import APIRouter
from app.api.v1.products import router as products_router
from app.api.v1.categories import router as categories_router
from app.api.v1.cart import router as cart_router
from app.api.v1.orders import router as orders_router
from app.api.v1.contact import router as contact_router
from app.api.v1.health import router as health_router

# Version 1 Master Router
router = APIRouter()

router.include_router(products_router)
router.include_router(categories_router)
router.include_router(cart_router)
router.include_router(orders_router)
router.include_router(contact_router)
router.include_router(health_router)
