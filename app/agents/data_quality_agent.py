class DataQualityAgent:

    REQUIRED_FIELDS = [
        "Air_temperature_K",
        "Process_temperature_K",
        "Rotational_speed_rpm",
        "Torque_Nm",
        "Tool_wear_min"
    ]

    def validate(self, data: dict):

        missing = []

        for field in self.REQUIRED_FIELDS:
            if field not in data:
                missing.append(field)

        if missing:
            return {
                "valid": False,
                "missing_fields": missing
            }

        return {"valid": True}