import random

random.seed(7)

RETRY_SUCCESS_RATE = 0.55
NUDGE_SUCCESS_RATE = 0.35


def execute_action(txn, decision):
    action = decision["action"]

    if action == "retry":
        success = random.random() < RETRY_SUCCESS_RATE
        return {
            "outcome": "recovered" if success else "still_failed",
            "amount_recovered": txn["amount"] if success else 0,
        }

    if action == "nudge":
        success = random.random() < NUDGE_SUCCESS_RATE
        return {
            "outcome": "recovered" if success else "no_response",
            "amount_recovered": txn["amount"] if success else 0,
        }

    if action == "escalate_human":
        return {
            "outcome": "escalated",
            "amount_recovered": 0,
        }

    return {
        "outcome": "no_action",
        "amount_recovered": 0,
    }