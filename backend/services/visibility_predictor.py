# services/visibility_predictor.py
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

class VisibilityPredictor:
    def __init__(self):
        self.model = self._build_model()
        # Load pre-trained weights here
    
    def _build_model(self):
        model = Sequential([
            LSTM(64, input_shape=(30, 5)),  # 30 days history, 5 features
            Dense(1, activation='sigmoid')  # Visibility probability
        ])
        model.compile(loss='binary_crossentropy', optimizer='adam')
        return model
    
    def predict(self, weather_data: np.ndarray) -> float:
        """Predict visibility (0-1) from weather data"""
        return float(self.model.predict(weather_data)[0][0])