import numpy as np


class ExplanationAgent:
    def __init__(self, model, explainer):
        self.model = model
        self.explainer = explainer
        self.feature_name_map = {
            "Air_temperature_K": "air temperature",
            "Process_temperature_K": "process temperature",
            "Rotational_speed_rpm": "rotational speed",
            "Torque_Nm": "torque",
            "Tool_wear_min": "tool wear",
            "Type_H": "high-grade machine type",
            "Type_L": "low-grade machine type",
            "Type_M": "medium-grade machine type",
            "temperature_difference": "temperature difference",
            "mechanical_stress": "mechanical stress",
            "wear_stress": "wear-related stress",
            "thermal_wear_stress": "thermal wear stress",
            "power_load": "power load",
        }

    def explain(self, sample, feature_names):
        shap_values = self.explainer.shap_values(sample)

        values = shap_values[0]
        importance = np.abs(values)

        top_indices = importance.argsort()[-3:][::-1]
        top_features_raw = [feature_names[i] for i in top_indices]
        top_features = [self.feature_name_map.get(f, f) for f in top_features_raw]

        explanation = (
            f"Failure risk is mainly influenced by "
            f"{top_features[0]}, {top_features[1]}, and {top_features[2]}."
        )

        return {
            "top_features": top_features,
            "explanation": explanation
        }