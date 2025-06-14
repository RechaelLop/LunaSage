class CropAlgorithms:
    @staticmethod
    def get_tomato_window(soil_temp: float) -> str:
        return "First Quarter" if soil_temp > 15 else "Wait for warmer soil"
    
    @staticmethod
    def get_potato_depth(moon_age: int) -> float:
        return (moon_age % 7) * 1.27  # cm
    
    @staticmethod
    def get_rice_water_adjustment(phase: str) -> str:
        return {
            "Waxing": "Increase water depth 1cm/day",
            "Waning": "Maintain current level",
            "Full": "Reduce slightly"
        }.get(phase, "Standard irrigation")