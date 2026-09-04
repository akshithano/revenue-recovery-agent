import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None


def write_recovery_message(txn, decision):
    if client is None:
        return fallback_message(txn, decision)

    prompt = f"""You are writing a short, polite payment recovery message to a customer.

Customer name: {txn['customer']}
Amount due: Rs {txn['amount']}
Reason for the message: {decision['reason']}
Action type: {decision['action']}

Write a message under 40 words. Be warm, not pushy. Do not mention internal
system details like 'prior attempts' or 'escalation'. If action_type is
'nudge' for an abandoned checkout, gently remind them their cart is waiting.
If it's for a card issue, ask them to update their payment method."""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        text = response.choices[0].message.content.strip()
        return text if text else fallback_message(txn, decision)
    except Exception:
        return fallback_message(txn, decision)


def fallback_message(txn, decision):
    return (
        f"Hi {txn['customer']}, we noticed an issue with your recent payment "
        f"of Rs {txn['amount']:.2f}. Please update your payment details or "
        f"contact support to complete it."
    )