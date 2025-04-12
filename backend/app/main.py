from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from app.config.settings import get_settings
from app.api.endpoints import router as endpoints_router  # Import the router correctly

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=get_settings().app_name,
    description="Zoku Backend Service",
    version="1.0.0",
)

# Get allowed origins from environment variables or use default for development
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
origins = [origin.strip() for origin in allowed_origins.split(",")]

# Configure CORS with specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes from other files
app.include_router(endpoints_router, prefix="/api")  # Add a prefix for API routes

@app.get("/")
async def read_root():
    return {"message": "Welcome to the API"}

@app.get("/api/health-check")
async def health_check():
    logger.info("Health check endpoint called")
    return {"status": "ok", "message": "Backend is running"}

@app.get("/api/test-error")
async def test_error():
    logger.error("Test error endpoint called")
    raise HTTPException(status_code=500, detail="Test error response")
