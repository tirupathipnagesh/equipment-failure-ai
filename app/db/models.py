from sqlalchemy import Column, Integer, Float, String, Text, DateTime
from sqlalchemy.sql import func

from app.db.base import Base


class PredictionLog(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    machine_type = Column(String, nullable=False)

    air_temperature_k = Column(Float, nullable=False)
    process_temperature_k = Column(Float, nullable=False)
    rotational_speed_rpm = Column(Float, nullable=False)
    torque_nm = Column(Float, nullable=False)
    tool_wear_min = Column(Float, nullable=False)

    failure_probability = Column(Float, nullable=False)
    failure_prediction = Column(Integer, nullable=False)

    explanation = Column(Text, nullable=False)
    recommendation = Column(String, nullable=False)
    alert_level = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    response = Column(Text, nullable=False)

    machine_type = Column(String, nullable=False)
    air_temperature_k = Column(Float, nullable=False)
    process_temperature_k = Column(Float, nullable=False)
    rotational_speed_rpm = Column(Float, nullable=False)
    torque_nm = Column(Float, nullable=False)
    tool_wear_min = Column(Float, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())