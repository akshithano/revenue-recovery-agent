MAX_RETRY_ATTEMPTS = 2
MAX_DISCOUNT_PERCENT = 10
STALE_TXN_DAYS = 5


def decide_action(txn):
    failure_type = txn["failure_type"]
    prior_attempts = int(txn["prior_attempts"])

    if prior_attempts >= MAX_RETRY_ATTEMPTS:
        return {
            "action": "escalate_human",
            "reason": f"Already attempted {prior_attempts} times (cap is {MAX_RETRY_ATTEMPTS}). Stopping automated attempts to avoid spamming the customer."
        }

    if failure_type in ("bank_timeout", "insufficient_funds"):
        return {
            "action": "retry",
            "reason": f"Failure type '{failure_type}' is often temporary. Attempt {prior_attempts + 1} of {MAX_RETRY_ATTEMPTS}."
        }

    if failure_type == "card_expired":
        return {
            "action": "nudge",
            "reason": "Card expired — retrying is pointless. Ask the customer to update their payment method."
        }

    if failure_type == "abandoned_checkout":
        return {
            "action": "nudge",
            "reason": "Checkout was abandoned, not failed. A reminder/incentive nudge is appropriate."
        }

    return {
        "action": "escalate_human",
        "reason": f"Unrecognized failure type '{failure_type}'. Not confident enough to act automatically."
    }