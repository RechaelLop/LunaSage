# LunaSage/backend/services/agriculture/base_recommender.py
import json
import os
from enum import Enum
from typing import Dict, Tuple, Optional
from dataclasses import dataclass

class MoonPhase(Enum):
    NEW = "New Moon"
    WAXING_CRESCENT = "Waxing Crescent"
    FIRST_QUARTER = "First Quarter"
    WAXING_GIBBOUS = "Waxing Gibbous"
    FULL = "Full Moon"
    WANING_GIBBOUS = "Waning Gibbous"
    LAST_QUARTER = "Last Quarter"
    WANING_CRESCENT = "Waning Crescent"

@dataclass
class CropRule:
    optimal_phases: list[MoonPhase]
    avoid_phases: list[MoonPhase]
    planting_notes: str
    lunar_benefits: str

class BaseRecommender:
    def __init__(self):
        self.crop_rules = self._load_crop_rules()
    
    def _load_crop_rules(self) -> Dict[str, CropRule]:
        """Load and validate crop rules from JSON"""
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        data_path = os.path.join(base_dir, "data", "crop_rules.json")
        
        with open(data_path) as f:
            raw_rules = json.load(f)
        
        return {
            crop: CropRule(
                optimal_phases=[MoonPhase(phase) for phase in data["optimal_phases"]],
                avoid_phases=[MoonPhase(phase) for phase in data.get("avoid_phases", [])],
                planting_notes=data["planting_notes"],
                lunar_benefits=data["lunar_benefits"]
            )
            for crop, data in raw_rules.items()
        }

    def get_base_recommendation(self, crop: str, current_phase: MoonPhase) -> Tuple[str, Dict]:
        """
        Core recommendation logic used by all other services
        Returns: (recommendation_status, details_dict)
        """
        if crop.lower() not in self.crop_rules:
            return "Crop not found", {}
        
        rule = self.crop_rules[crop.lower()]
        
        if current_phase in rule.optimal_phases:
            return "OPTIMAL", {
                "message": f"Perfect time to plant {crop}",
                "actions": ["Prepare soil", "Sow seeds"],
                "confidence": 0.9
            }
        elif current_phase in rule.avoid_phases:
            return "AVOID", {
                "message": f"Unsuitable phase for {crop}",
                "alternative_actions": ["Soil preparation", "Weeding"],
                "risk": 0.8
            }
        else:
            return "NEUTRAL", {
                "message": f"Acceptable but not ideal for {crop}",
                "optimal_phases": [phase.value for phase in rule.optimal_phases],
                "confidence": 0.5
            }

    def is_phase_coming_soon(self, target: MoonPhase, current: MoonPhase) -> bool:
        """Utility method for phase prediction"""
        phase_order = list(MoonPhase)
        current_idx = phase_order.index(current)
        target_idx = phase_order.index(target)
        return (target_idx > current_idx) and (target_idx - current_idx <= 3)