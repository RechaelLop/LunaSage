from fastapi import APIRouter
from backend.services.lunar_events import lunar_service

router = APIRouter(prefix="/api/v1", tags=["Astronomy"])

@router.get("/moon/current")
async def current_moon_phase():
    """Get current moon phase with illumination percentage"""
    return lunar_service.get_current_phase()

@router.get("/moon/next-phases")
async def next_moon_phases(count: int = 4):
    """Get upcoming moon phases (default: next 4)"""
    return lunar_service._get_next_phases(ts.now(), count)