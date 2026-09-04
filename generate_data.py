

import random
import csv
from datetime import datetime, timedelta

random.seed(42)  

FAILURE_TYPES = [
    "insufficient_funds",
    "bank_timeout",
    "card_expired",
    "abandoned_checkout",
]

CUSTOMER_NAMES = [
    "Ravi Kumar", "Priya Singh", "Amit Sharma", "Sneha Patel", "Vikram Rao",
    "Ananya Iyer", "Karan Mehta", "Divya Nair", "Rohan Gupta", "Neha Joshi",
]

def generate_transactions(n=60):
    rows = []
    for i in range(1, n + 1):
        txn_id = f"TXN{1000 + i}"
        customer = random.choice(CUSTOMER_NAMES)
        amount = round(random.uniform(299, 15000), 2)
        failure_type = random.choice(FAILURE_TYPES)
        ts = datetime.now() - timedelta(
            days=random.randint(0, 7),
            hours=random.randint(0, 23)
        )
        prior_attempts = random.choice([0, 0, 0, 1, 1, 2])

        rows.append({
            "txn_id": txn_id,
            "customer": customer,
            "amount": amount,
            "failure_type": failure_type,
            "timestamp": ts.isoformat(),
            "prior_attempts": prior_attempts,
        })
    return rows


if __name__ == "__main__":
    data = generate_transactions(60)
    with open("transactions.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"Created transactions.csv with {len(data)} synthetic transactions.")