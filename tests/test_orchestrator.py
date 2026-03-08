from app.core.orchestrator import MaintenanceOrchestrator


orchestrator = MaintenanceOrchestrator()

sample_input = {
    "Type": "M",
    "Air_temperature_K": 300.5,
    "Process_temperature_K": 309.8,
    "Rotational_speed_rpm": 1345,
    "Torque_Nm": 62.7,
    "Tool_wear_min": 153
}

result = orchestrator.run(
    data=sample_input,
    question="Why is this machine risky?"
)

print(result)