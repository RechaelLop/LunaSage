import json
import os
from enum import Enum
from typing import Dict, Tuple, Union
from dataclasses import dataclass
from services.agriculture.base_recommender import BaseRecommender

class MoonPhase(Enum):
    NEW = "new moon"
    WAXING_CRESCENT = "waxing crescent"
    FIRST_QUARTER = "first quarter"
    WAXING_GIBBOUS = "waxing gibbous"
    FULL = "full moon"
    WANING_GIBBOUS = "waning gibbous"
    LAST_QUARTER = "last quarter"
    WANING_CRESCENT = "waning crescent"

@dataclass
class CropRecommendation:
    status: str
    message: str
    details: dict
    optimal_phase: str

class AgricultureService:
    def __init__(self):
        self.base = BaseRecommender()
        self.rules = self._load_rules()
    
    def _load_rules(self) -> Dict:
        """Load crop rules from JSON file"""
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        data_path = os.path.join(base_dir, "data", "crop_rules.json")
        
        with open(data_path) as f:
            return json.load(f)
    
    def get_recommendation(self, crop: str, current_phase: Union[str, MoonPhase] = None) -> CropRecommendation:
        """
        Unified recommendation method that combines both approaches
        Args:
            crop: Name of the crop
            current_phase: Either string phase name or MoonPhase enum
        Returns:
            CropRecommendation dataclass with all details
        """
        # Convert phase to enum if needed
        phase_enum = self._normalize_phase(current_phase)
        
        # Get base recommendation from shared logic
        base_status, base_details = self.base.get_base_recommendation(crop, phase_enum)
        
        # Get legacy recommendation details
        legacy_rec = self._get_legacy_recommendation(crop, phase_enum.value)
        
        return CropRecommendation(
            status=base_status,
            message=legacy_rec[0],
            details={
                **base_details,
                "legacy_notes": legacy_rec[1],
                "optimal_phase": self.rules.get(crop.lower(), {}).get("optimal_phase", "unknown")
            },
            optimal_phase=self.rules.get(crop.lower(), {}).get("optimal_phase", "unknown")
        )
    
    def _normalize_phase(self, phase: Union[str, MoonPhase]) -> MoonPhase:
        """Ensure we always work with MoonPhase enum"""
        if phase is None:
            return self._get_current_phase()
        return phase if isinstance(phase, MoonPhase) else MoonPhase(phase.lower())
    
    def _get_current_phase(self) -> MoonPhase:
        """Connect to lunar service"""
        phase_data = lunar_service.get_current_phase()  # Your existing call
        return MoonPhase(phase_data['phase'].lower())
    
    def _get_legacy_recommendation(self, crop: str, current_phase: str) -> Tuple[str, str]:
        """Maintains your original method's behavior"""
        crop = crop.lower().strip()
        if crop not in self.rules:
            return "N/A", "Crop not in database"
        
        recommended_phase = self.rules[crop]["optimal_phase"].lower()
        
        if current_phase.lower() in recommended_phase:
            return "Ideal planting time", self.rules[crop]["reasoning"]
        elif self._is_phase_coming_soon(current_phase, recommended_phase):
            return f"Prepare for {recommended_phase}", self.rules[crop]["preparation_advice"]
        else:
            return f"Wait for {recommended_phase}", self.rules[crop]["alternative_tasks"]
    
    def _is_phase_coming_soon(self, current: str, target: str) -> bool:
        """Your original phase comparison logic"""
        phase_order = [p.value for p in MoonPhase]
        try:
            return phase_order.index(target) > phase_order.index(current)
        except ValueError:
            return False
    
    # Maintain backward compatibility
    def get_planting_recommendation(self, crop: str, current_phase: str) -> Tuple[str, str]:
        """Original method preserved exactly"""
        return self._get_legacy_recommendation(crop, current_phase)