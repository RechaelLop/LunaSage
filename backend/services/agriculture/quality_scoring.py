from enum import Enum

class MoonScore(Enum):
    POOR = 1
    FAIR = 3
    GOOD = 5
    EXCELLENT = 8

def get_crop_score(crop: str, phase: str) -> MoonScore:
    scoring = {
        'tomato': {"New": 2, "Waxing": 8, "Full": 4, "Waning": 5},
        'potato': {"New": 5, "Waxing": 3, "Full": 2, "Waning": 9}
    }
    return MoonScore(scoring.get(crop, {}).get(phase, 5))