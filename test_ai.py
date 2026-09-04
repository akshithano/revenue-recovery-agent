import csv
from rules_engine import decide_action
from ai_messenger import write_recovery_message

with open("transactions.csv", "r") as f:
    reader = csv.DictReader(f)
    transactions = list(reader)

txn = transactions[0]
txn["amount"] = float(txn["amount"])

decision = decide_action(txn)
print(f"Transaction: {txn['txn_id']} | Action: {decision['action']}")
print(f"Reason: {decision['reason']}")
print()

message = write_recovery_message(txn, decision)
print("AI-generated message:")
print(message)