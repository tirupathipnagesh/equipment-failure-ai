import joblib
import shap
import pandas as pd
import numpy as np

from app.agents.data_quality_agent import DataQualityAgent
from app.agents.prediction_agent import PredictionAgent
from app.agents.explanation_agent import ExplanationAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.alert_agent import AlertAgent
from app.agents.chatbot_agent import ChatbotAgent


class MaintenanceOrchestrator:
    def __init__(self, model_path: str = "models/failure_model_clean.pkl"):
        self.data_quality_agent = DataQualityAgent()
        self.prediction_agent = PredictionAgent(model_path=model_path)

        self.model = self.prediction_agent.model
        self.explainer = shap.TreeExplainer(self.model)

        self.planner_agent = PlannerAgent()
        self.alert_agent = AlertAgent()
        self.chatbot_agent = ChatbotAgent()

        self.feature_names = [
            "Air_temperature_K",
            "Process_temperature_K",
            "Rotational_speed_rpm",
            "Torque_Nm",
            "Tool_wear_min",
            "Type_H",
            "Type_L",
            "Type_M",
            "temperature_difference",
            "mechanical_stress",
            "wear_stress",
            "thermal_wear_stress",
            "power_load"
        ]

        self.explanation_agent = ExplanationAgent(
            model=self.model,
            explainer=self.explainer
        )

    def prepare_features(self, data: dict) -> dict:
        machine_type = data.get("Type", "M")

        type_h = 1 if machine_type == "H" else 0
        type_l = 1 if machine_type == "L" else 0
        type_m = 1 if machine_type == "M" else 0

        air_temp = data["Air_temperature_K"]
        process_temp = data["Process_temperature_K"]
        rotational_speed = data["Rotational_speed_rpm"]
        torque = data["Torque_Nm"]
        tool_wear = data["Tool_wear_min"]

        prepared = {
            "Air_temperature_K": air_temp,
            "Process_temperature_K": process_temp,
            "Rotational_speed_rpm": rotational_speed,
            "Torque_Nm": torque,
            "Tool_wear_min": tool_wear,
            "Type_H": type_h,
            "Type_L": type_l,
            "Type_M": type_m,
            "temperature_difference": process_temp - air_temp,
            "mechanical_stress": torque * rotational_speed,
            "wear_stress": tool_wear * torque,
            "thermal_wear_stress": process_temp * tool_wear,
            "power_load": (torque * rotational_speed) / 1000
        }

        return prepared

    def run(self, data: dict, question: str | None = None):
        validation = self.data_quality_agent.validate(data)
        if not validation["valid"]:
            return {
                "status": "error",
                "message": "Invalid input data",
                "details": validation
            }

        features = self.prepare_features(data)

        prediction_result = self.prediction_agent.predict_failure(features)
        failure_probability = prediction_result["failure_probability"]

        sample_df = pd.DataFrame([features], columns=self.feature_names).astype("float64")

        explanation_result = self.explanation_agent.explain(
            sample=sample_df.values,
            feature_names=self.feature_names
        )

        recommendation = self.planner_agent.recommend(failure_probability)
        alert = self.alert_agent.generate_alert(failure_probability)

        response = {
            "status": "success",
            "failure_probability": failure_probability,
            "failure_prediction": prediction_result["failure_prediction"],
            "top_features": explanation_result["top_features"],
            "explanation": explanation_result["explanation"],
            "recommendation": recommendation,
            "alert_level": alert["level"]
        }

        if question:
            chatbot_response = self.chatbot_agent.answer(question, response)
            response["chatbot_response"] = chatbot_response

        return response