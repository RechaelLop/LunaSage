from skyfield.api import load, Topos
from skyfield.almanac import moon_phases, find_discrete
from datetime import datetime, timedelta
from typing import Dict, List
import math

# Load ephemeris once (better performance)
eph = load('de421.bsp')
ts = load.timescale()

class LunarEvents:
    def __init__(self):
        self.sun = eph['sun']
        self.moon = eph['moon']
        self.earth = eph['earth']

    def get_current_phase(self) -> Dict[str, float]:
        """Get current moon phase with illumination percentage"""
        t = ts.now()
        phase_name = self._calculate_phase(t)
        illumination = self._calculate_illumination(t)
        
        return {
            "phase": phase_name,
            "illumination": illumination,
            "timestamp": t.utc_strftime("%Y-%m-%d %H:%M:%S"),
            "next_phases": self._get_next_phases(t)
        }

    def _calculate_phase(self, t) -> str:
        """More precise phase calculation using ecliptic longitude"""
        e = self.earth.at(t)
        s = e.observe(self.sun).apparent()
        m = e.observe(self.moon).apparent()
        
        angle = (m.ecliptic_latlon()[1].degrees - s.ecliptic_latlon()[1].degrees) % 360
        illumination = (1 - math.cos(math.radians(angle)))/2
        
        if illumination < 0.02: return "New Moon"
        elif angle < 90: return "Waxing Crescent"
        elif angle < 135: return "First Quarter"
        elif angle < 180: return "Waxing Gibbous"
        elif illumination > 0.98: return "Full Moon"
        elif angle < 270: return "Waning Gibbous"
        elif angle < 315: return "Last Quarter"
        else: return "Waning Crescent"

    def _calculate_illumination(self, t) -> float:
        """Calculate exact illumination percentage (0-100)"""
        e = self.earth.at(t)
        s = e.observe(self.sun).apparent()
        m = e.observe(self.moon).apparent()
        angle = s.separation_from(m).radians
        return round(50 * (1 - math.cos(angle)), 1)

    def _get_next_phases(self, t, count=4) -> List[Dict]:
        """Get upcoming moon phases"""
        t1 = t + timedelta(days=60)  # Next 2 months
        phase_times, phase_indices = find_discrete(t, t1, moon_phases(eph))
        
        phases = []
        phase_names = ["New Moon", "First Quarter", "Full Moon", "Last Quarter"]
        for ti, yi in zip(phase_times[:count], phase_indices[:count]):
            phases.append({
                "phase": phase_names[yi],
                "date": ti.utc_strftime("%Y-%m-%d %H:%M"),
                "illumination": 50 if "Quarter" in phase_names[yi] else 
                               100 if "Full" in phase_names[yi] else 0
            })
        return phases

# Singleton service instance
lunar_service = LunarEvents()