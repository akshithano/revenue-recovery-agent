import csv
from rules_engine import decide_action
from simulate_execution import execute_action
from ai_messenger import write_recovery_message

INPUT_FILE = "transactions.csv"
AUDIT_FILE = "audit_trail.csv"


def load_transactions(path):
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)


def run_batch(transactions):
    audit_rows = []

    for txn in transactions:
        txn["amount"] = float(txn["amount"])

        decision = decide_action(txn)
        result = execute_action(txn, decision)

        message = ""
        if decision["action"] == "nudge":
            message = write_recovery_message(txn, decision)

        audit_rows.append({
            "txn_id": txn["txn_id"],
            "customer": txn["customer"],
            "amount": txn["amount"],
            "failure_type": txn["failure_type"],
            "prior_attempts": txn["prior_attempts"],
            "action_taken": decision["action"],
            "reason": decision["reason"],
            "outcome": result["outcome"],
            "amount_recovered": result["amount_recovered"],
            "ai_message": message,
        })

    return audit_rows


def save_audit_trail(rows, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


def print_summary(rows):
    total_at_risk = sum(r["amount"] for r in rows)
    total_recovered = sum(r["amount_recovered"] for r in rows)
    escalated = [r for r in rows if r["action_taken"] == "escalate_human"]
    nudged = [r for r in rows if r["action_taken"] == "nudge"]

    print("=" * 50)
    print("REVENUE RECOVERY SUMMARY")
    print("=" * 50)
    print(f"Transactions processed : {len(rows)}")
    print(f"Total revenue at risk  : Rs {total_at_risk:,.2f}")
    print(f"Total revenue recovered: Rs {total_recovered:,.2f}")
    print(f"Recovery rate          : {(total_recovered/total_at_risk)*100:.1f}%")
    print(f"Escalated to human      : {len(escalated)} transactions")
    print(f"AI messages generated   : {len(nudged)} transactions")
    print("=" * 50)


if __name__ == "__main__":
    transactions = load_transactions(INPUT_FILE)
    audit_rows = run_batch(transactions)
    save_audit_trail(audit_rows, AUDIT_FILE)
    print_summary(audit_rows)
    print(f"\nFull audit trail saved to {AUDIT_FILE}")