import numpy as np

class PlantingOptimizer:
    """Determines optimal planting days combining lunar + weather data"""
    
    def __init__(self):
        self.weather_weights = {
            'temperature': 0.4,
            'precipitation': 0.3,
            'moon_phase': 0.3
        }
    
    def calculate_optimal_day(self, forecast_data: dict, moon_phase: str) -> float:
        """Returns 0-1 score for planting suitability"""
        temp_score = np.interp(forecast_data['temp'], [10, 25], [0, 1])
        rain_score = 0 if forecast_data['rain'] > 5 else 1
        moon_score = 0.8 if moon_phase in ["Waxing Crescent", "First Quarter"] else 0.5
        
        return (temp_score * self.weather_weights['temperature'] +
                rain_score * self.weather_weights['precipitation'] +
                moon_score * self.weather_weights['moon_phase'])