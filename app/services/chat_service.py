from sqlalchemy.orm import Session

from app.db.models import ChatLog


def save_chat_log(db: Session, question: str, input_data: dict, response: str):
    record = ChatLog(
        question=question,
        response=response,
        machine_type=input_data["Type"],
        air_temperature_k=input_data["Air_temperature_K"],
        process_temperature_k=input_data["Process_temperature_K"],
        rotational_speed_rpm=input_data["Rotational_speed_rpm"],
        torque_nm=input_data["Torque_Nm"],
        tool_wear_min=input_data["Tool_wear_min"],
    )

    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def format_chat_context(result: dict) -> dict:
    return {
        "status": result["status"],
        "failure_probability": result["failure_probability"],
        "failure_prediction": result["failure_prediction"],
        "explanation": result["explanation"],
        "recommendation": result["recommendation"],
        "alert_level": result["alert_level"],
        "chatbot_response": result.get("chatbot_response", "")
    }