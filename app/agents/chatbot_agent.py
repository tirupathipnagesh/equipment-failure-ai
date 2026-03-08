from app.services.llm_service import LLMService


class ChatbotAgent:
    def __init__(self):
        self.llm_service = None
        try:
            self.llm_service = LLMService()
            print("LLMService initialized successfully.")
        except Exception as e:
            print(f"LLMService initialization failed: {e}")
            self.llm_service = None

    def detect_intent(self, question: str) -> str:
        q = question.lower()

        explanation_words = [
            "why",
            "reason",
            "cause",
            "explain",
            "factor",
            "contributing",
            "influence",
            "driver",
        ]

        risk_words = [
            "risk",
            "probability",
            "chance",
            "likelihood",
        ]

        recommendation_words = [
            "recommend",
            "maintenance",
            "action",
            "do now",
            "fix",
        ]

        alert_words = [
            "alert",
            "severity",
            "critical",
            "warning",
        ]

        if any(word in q for word in explanation_words):
            return "explanation"

        if any(word in q for word in risk_words):
            return "risk"

        if any(word in q for word in recommendation_words):
            return "recommendation"

        if any(word in q for word in alert_words):
            return "alert"

        return "summary"

    def fallback_answer(self, question: str, context: dict) -> str:
        intent = self.detect_intent(question)

        probability = context.get("failure_probability", 0.0)
        prediction = context.get("failure_prediction", 0)
        explanation = context.get("explanation", "")
        recommendation = context.get("recommendation", "")
        alert_level = context.get("alert_level", "UNKNOWN")
        top_features = context.get("top_features", [])

        risk_percent = round(probability * 100, 2)

        if intent == "explanation":
            features_text = ", ".join(top_features) if top_features else "the main sensor features"
            return (
                f"The model indicates {'elevated' if prediction == 1 else 'low'} failure risk. "
                f"The most influential factors are {features_text}. "
                f"{explanation}"
            )

        if intent == "risk":
            return (
                f"The estimated failure probability is {risk_percent}%. "
                f"The current prediction is "
                f"{'failure risk detected' if prediction == 1 else 'no immediate failure risk'}."
            )

        if intent == "recommendation":
            return f"Recommended action: {recommendation}."

        if intent == "alert":
            return f"The current alert level is {alert_level}."

        if intent == "summary":
            return (
                f"Machine summary: failure probability is {risk_percent}%, "
                f"alert level is {alert_level}, and recommended action is: {recommendation}."
            )

        return (
            "I can help explain the machine risk, failure probability, "
            "alert level, and recommended maintenance action."
        )

    def answer(self, question: str, context: dict) -> str:
        if self.llm_service:
            try:
                response = self.llm_service.generate_response(question, context)
                print("LLM response generated successfully.")
                return response
            except Exception as e:
                print(f"LLM response generation failed: {e}")

        print("Using fallback chatbot response.")
        return self.fallback_answer(question, context)