from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from database import create_tables, get_db
from routers import auth, admin
from dependencies import get_current_user
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI application
app = FastAPI(
    title="Comics Timeline OAuth2 Proxy",
    description="OAuth2 Authentication service for Comics Timeline application",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8000"],  # Frontend and main backend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()

# Include routers
app.include_router(auth.router)
app.include_router(admin.router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Comics Timeline OAuth2 Proxy",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "oauth-proxy"}

# Protected test endpoint
@app.get("/protected")
async def protected_endpoint(current_user = Depends(get_current_user)):
    return {
        "message": "This is a protected endpoint",
        "user": current_user.username,
        "user_id": current_user.id
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
