from pydantic import BaseModel, Field
from typing import Optional


class ChatQueryRequest(BaseModel):
    question: str = Field(..., example="Why is this machine risky?")
    Type: str = Field(..., example="M")
    Air_temperature_K: float = Field(..., example=300.5)
    Process_temperature_K: float = Field(..., example=309.8)
    Rotational_speed_rpm: float = Field(..., example=1345)
    Torque_Nm: float = Field(..., example=62.7)
    Tool_wear_min: float = Field(..., example=153)


class ChatQueryResponse(BaseModel):
    status: str
    chatbot_response: str
    failure_probability: float
    failure_prediction: int
    explanation: str
    recommendation: str
    alert_level: str