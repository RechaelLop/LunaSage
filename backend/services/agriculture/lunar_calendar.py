from datetime import datetime
from typing import Dict

class LunarCalendar:
    def __init__(self):
        self.crop_dates = self._load_crop_dates()
    
    def _load_crop_dates(self) -> Dict:
        # Connect to your crop_rules.json or external API
        return {
            'tomato': {
                'optimal': ["2023-04-03", "2023-05-02"],
                'avoid': ["2023-06-10"]
            }
        }
    
    def get_dates(self, crop: str, year: int = None) -> Dict:
        return self.crop_dates.get(crop.lower(), {})