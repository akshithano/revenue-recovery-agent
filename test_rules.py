import csv
from rules_engine import decide_action

with open("transactions.csv", "r") as f:
    reader = csv.DictReader(f)
    transactions = list(reader)

for txn in transactions[:10]:
    decision = decide_action(txn)
    print(f"{txn['txn_id']} | {txn['failure_type']} | prior={txn['prior_attempts']} -> {decision['action']}")
    print(f"   reason: {decision['reason']}")
    print()