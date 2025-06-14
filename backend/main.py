from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from datetime import datetime
from backend.routers import planting_dates
from backend.services import agriculture
from backend.routers import moon

app = FastAPI(
    title="LunaSage API",
    description="Lunar agricultural advisor with astronomical predictions",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Agriculture",
            "description": "Moon phase-based planting recommendations"
        },
        {
            "name": "System",
            "description": "Health checks and monitoring"
        }
    ]
)

# Include routers
app.include_router(moon.router)
app.include_router(planting_dates.router)

@app.get("/health", tags=["System"], summary="System Health Status")
async def health_check():
    """Check system health and service availability
    
    Returns:
        dict: System health status including:
            - Service status
            - Version info
            - System metrics
            - Dependency status
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "services": {
            "astronomy": {
                "status": "operational",
                "last_updated": datetime.utcnow().isoformat() + "Z"
            },
            "agriculture": {
                "status": "operational",
                "rules_loaded": len(agriculture_service.rules["crops"])
            }
        },
        "system": {
            "cpu_usage": f"{psutil.cpu_percent()}%",
            "memory_usage": f"{psutil.virtual_memory().percent}%",
            "uptime": f"{psutil.boot_time()} seconds"
        },
        "links": {
            "documentation": "/docs",
            "api_spec": "/openapi.json"
        }
    }

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exc),
            "type": "value_error",
            "status": 400
        }
    )

@app.get("/")
async def root():
    return {
        "message": "LunaSage Agricultural Advisor",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "planting_dates": "/api/v1/planting-dates"
        }
    }