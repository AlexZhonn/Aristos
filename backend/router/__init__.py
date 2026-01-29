from .auth import router as auth_router
from .receipts import router as receipts_router
from .pantry import router as pantry_router
from .comparison import router as comparison_router
from .analytics import router as analytics_router
from .notifications import router as notifications_router

__all__ = [
    "auth_router",
    "receipts_router",
    "pantry_router",
    "comparison_router",
    "analytics_router",
    "notifications_router",
]
