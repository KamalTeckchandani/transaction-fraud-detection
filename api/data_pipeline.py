import time
from utils.data_generator import generate_transaction
from utils.fraud_rules import detect_rules
from utils.genai_explain import generate_explanation  # comment if not using GenAI
from models.db_models import Transaction, Alert, init_db, get_session



BLACKLIST = set()
USER_HISTORY = {}
engine = init_db()
session = get_session(engine)

def vectorize_transaction(tx):
    # Example: [amount, velocity, hour] – replace with your actual feature extraction
    amount = tx['amount']
    velocity = len(USER_HISTORY.get(tx['user_id'], []))
    hour = tx['timestamp'].hour
    return [amount, velocity, hour]

def pipeline_loop():
    while True:
        tx = generate_transaction()
        user_id = tx['user_id']
        USER_HISTORY.setdefault(user_id, []).append(tx)

        # Rule-based detection
        risk_score, reasons = detect_rules(tx, USER_HISTORY, BLACKLIST)
        
        # Optional: ML anomaly detection code here (load model, pass features, etc.)

        # GenAI explanation (optional)
        explanation = None
        if reasons:
            try:
                explanation = generate_explanation(tx, reasons)
            except:
                explanation = ', '.join(reasons)

        # Save transaction
        t_row = Transaction(**tx)
        session.add(t_row)
        
        # Save alert if flagged
        if risk_score > 0:
            a_row = Alert(
                transaction_id=tx['transaction_id'],
                risk_score=risk_score,
                reasons=', '.join(reasons),
                explanation=explanation
            )
            session.add(a_row)
        
        session.commit()
        print(f"Processed: {tx['transaction_id']}, Score: {risk_score}, Reasons: {reasons}, Explanation: {explanation}")
        time.sleep(2)  # Adjust for how “live” you want it

if __name__ == "__main__":
    pipeline_loop()
