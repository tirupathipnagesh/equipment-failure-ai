from sqlalchemy.orm import Session

from app.db.models import PredictionLog


def save_prediction(db: Session, input_data: dict, result: dict):
    record = PredictionLog(
        machine_type=input_data["Type"],
        air_temperature_k=input_data["Air_temperature_K"],
        process_temperature_k=input_data["Process_temperature_K"],
        rotational_speed_rpm=input_data["Rotational_speed_rpm"],
        torque_nm=input_data["Torque_Nm"],
        tool_wear_min=input_data["Tool_wear_min"],
        failure_probability=result["failure_probability"],
        failure_prediction=result["failure_prediction"],
        explanation=result["explanation"],
        recommendation=result["recommendation"],
        alert_level=result["alert_level"],
    )

    db.add(record)
    db.commit()
    db.refresh(record)
    return record