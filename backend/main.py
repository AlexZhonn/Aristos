from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import routers
from router import (
    auth_router,
    receipts_router,
    pantry_router,
    comparison_router,
    analytics_router,
    notifications_router
)

app = FastAPI(
    title="Aristos API",
    description="Smart Calorie & Budget Manager API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(receipts_router)
app.include_router(pantry_router)
app.include_router(comparison_router)
app.include_router(analytics_router)
app.include_router(notifications_router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Aristos API",
        "version": "1.0.0",
        "status": "online"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Start background tasks on startup
@app.on_event("startup")
async def startup_event():
    """Initialize services and start background tasks"""
    print("🚀 Aristos API starting up...")
    print("📱 Backend ready to serve requests")
    # Background tasks for notifications will be handled separately


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("👋 Aristos API shutting down...")
