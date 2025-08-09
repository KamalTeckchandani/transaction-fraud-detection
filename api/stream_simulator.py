import time
from utils.data_generator import generate_transaction
from utils.fraud_rules import detect_rules

BLACKLIST = set()  # Populate with user_ids or ips if any
USER_HISTORY = {}

def simple_stream():
    while True:
        tx = generate_transaction()
        user_id = tx['user_id']
        
        USER_HISTORY.setdefault(user_id, []).append(tx)
        
        risk_score, reasons = detect_rules(tx, USER_HISTORY, BLACKLIST)
        
        print(f"Transaction ID: {tx['transaction_id']} Risk Score: {risk_score} Reasons: {reasons}")
        
        time.sleep(2)  # Wait 2 seconds between transactions

if __name__ == "__main__":
    simple_stream()
