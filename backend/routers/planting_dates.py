from fastapi import APIRouter, Query, HTTPException
from backend.services.agriculture import AgricultureService, MoonPhase
from backend.services.lunar_events import get_current_moon_phase
from typing import Optional
import warnings

router = APIRouter(prefix="/api/v1", tags=["Agriculture"])
service = AgricultureService()

@router.get("/planting-recommendations", summary="Get comprehensive planting recommendations")
async def get_planting_recommendations(
    crop: str = Query(..., description="Crop name (e.g., tomato, carrot)"),
    location: Optional[str] = Query(None, description="Optional location for regional adjustments"),
    date: Optional[str] = Query(None, description="Optional date (YYYY-MM-DD) for future planning"),
    include_basic: bool = Query(False, description="Include legacy response format")
):
    """
    Get lunar agriculture recommendations with enhanced details.
    
    Returns both modern recommendations and optionally the legacy format.
    """
    try:
        # Get current or specified moon phase
        current_phase = get_current_moon_phase(date) if date else get_current_moon_phase()
        
        # Get modern recommendation
        recommendation = service.get_recommendation(crop, current_phase)
        
        response = {
            "crop": crop.title(),
            "location": location,
            "current_moon_phase": current_phase,
            "recommendation": recommendation.message,
            "details": {
                "optimal_phase": recommendation.optimal_phase,
                "lunar_benefits": service.rules.get(crop.lower(), {}).get("lunar_benefits", ""),
                **recommendation.details
            }
        }
        
        # Include legacy format if requested
        if include_basic:
            warnings.warn("Legacy format is deprecated", DeprecationWarning)
            basic_rec = service.get_planting_recommendation(crop, current_phase)
            response["legacy_format"] = {
                "window": basic_rec[0],
                "notes": basic_rec[1]
            }
            
        return response
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/planting-dates", deprecated=True)
async def get_planting_dates_legacy(
    crop: str = Query(...),
    location: str = Query(None)
):
    """
    DEPRECATED: Legacy endpoint - use /planting-recommendations instead
    
    Returns basic planting window information.
    """
    warnings.warn("Endpoint deprecated - use /planting-recommendations", DeprecationWarning)
    try:
        current_phase = get_current_moon_phase()
        window, notes = service.get_planting_recommendation(crop, current_phase)
        
        return {
            "crop": crop,
            "location": location,
            "current_moon_phase": current_phase,
            "recommended_window": window,
            "notes": notes,
            "meta": {
                "migration_notice": "Switch to /planting-recommendations",
                "new_endpoint": f"/api/v1/planting-recommendations?crop={crop}"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))