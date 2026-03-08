class PlannerAgent:

    def recommend(self, probability):

        if probability > 0.8:
            return "Immediate maintenance required"

        if probability > 0.6:
            return "Schedule inspection soon"

        if probability > 0.4:
            return "Monitor machine condition"

        return "Machine operating normally"