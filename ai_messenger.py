import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def write_recovery_message(txn, decision):
    prompt = f"""You are writing a short, polite payment recovery message to a customer.

Customer name: {txn['customer']}
Amount due: Rs {txn['amount']}
Reason for the message: {decision['reason']}
Action type: {decision['action']}

Write a message under 40 words. Be warm, not pushy. Do not mention internal
system details like 'prior attempts' or 'escalation'. If action_type is
'nudge' for an abandoned checkout, gently remind them their cart is waiting.
If it's for a card issue, ask them to update their payment method."""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    print("RAW RESPONSE (debug):", response)  # temporary, so we can see what's happening

    return response.choices[0].message.content.strip()