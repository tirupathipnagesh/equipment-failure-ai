from pydantic import BaseModel, Field
from typing import List


class FailurePredictionRequest(BaseModel):
    Type: str = Field(..., example="M")
    Air_temperature_K: float = Field(..., example=300.5)
    Process_temperature_K: float = Field(..., example=309.8)
    Rotational_speed_rpm: float = Field(..., example=1345)
    Torque_Nm: float = Field(..., example=62.7)
    Tool_wear_min: float = Field(..., example=153)


class FailurePredictionResponse(BaseModel):
    status: str
    failure_probability: float
    failure_prediction: int
    top_features: List[str]
    explanation: str
    recommendation: str
    alert_level: str