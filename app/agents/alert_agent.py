class AlertAgent:

    def generate_alert(self, probability):

        if probability > 0.8:
            return {"level": "CRITICAL"}

        if probability > 0.6:
            return {"level": "WARNING"}

        if probability > 0.4:
            return {"level": "INFO"}

        return {"level": "NORMAL"}