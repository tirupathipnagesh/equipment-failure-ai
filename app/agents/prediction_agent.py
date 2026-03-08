import joblib
import numpy as np


class PredictionAgent:
    def __init__(self, model_path="models/failure_model_clean.pkl"):
        self.model = joblib.load(model_path)

    def predict_failure(self, features: dict):
        X = np.array(list(features.values()), dtype=float).reshape(1, -1)

        probability = self.model.predict_proba(X)[0][1]
        prediction = int(probability > 0.5)

        return {
            "failure_probability": float(probability),
            "failure_prediction": prediction
        }