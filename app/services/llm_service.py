from openai import OpenAI

from app.core.config import settings


class LLMService:
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set")

        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate_response(self, question: str, context: dict) -> str:
        prompt = f"""
You are an industrial predictive maintenance assistant that should respond in a natural,
clear, helpful, and human-like way, similar to ChatGPT.

Your job is to answer the user's question using ONLY the provided machine context.

Rules:
- Do not invent values or facts
- Do not mention information not present in the context
- Write naturally, not like a rigid template
- Sound like an intelligent assistant helping an engineer or operator
- If the machine is low risk, say that clearly
- If the user asks about causes, mention the top contributing factors
- If the user asks for recommendations, explain what should be done in practical terms
- Keep responses conversational but professional
- Use complete sentences and natural phrasing
- Avoid sounding repetitive or robotic

Machine context:
- failure_probability: {context.get('failure_probability')}
- failure_prediction: {context.get('failure_prediction')}
- top_features: {context.get('top_features')}
- explanation: {context.get('explanation')}
- recommendation: {context.get('recommendation')}
- alert_level: {context.get('alert_level')}

User question:
{question}
"""

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful predictive maintenance assistant. "
                        "Respond naturally and clearly like ChatGPT, but stay grounded in the provided machine context."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.5,
        )

        return response.choices[0].message.content.strip()