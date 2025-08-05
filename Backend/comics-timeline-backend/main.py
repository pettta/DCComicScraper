from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import accounts, books, timeline

# Create FastAPI application
app = FastAPI(
    title="DC Comics Price Checker API",
    description="API for managing DC Comics collection and pricing data",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vue.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(accounts.router)
app.include_router(books.router)
app.include_router(timeline.router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to DC Comics Price Checker API",
        "docs": "/docs",
        "health": "OK"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "dc-comics-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
