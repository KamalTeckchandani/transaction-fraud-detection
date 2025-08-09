def detect_rules(transaction, user_history, blacklist):
    risk_score = 0
    reasons = []

    # High amount
    if transaction['amount'] > 3000:
        risk_score += 30
        reasons.append("High amount")

    user_id = transaction['user_id']

    # High frequency — simplistic example: count recent transactions
    if user_id in user_history:
        recent_txns = user_history[user_id]
        if len(recent_txns) >= 5:
            risk_score += 40
            reasons.append("High frequency of transactions")

    # Simple IP vs location mismatch — placeholder logic
    if transaction['location'] not in transaction['ip_address']:
        risk_score += 20
        reasons.append("IP and location mismatch")

    # Blacklist check
    if user_id in blacklist or transaction['ip_address'] in blacklist:
        risk_score += 50
        reasons.append("Blacklisted user or IP")

    return risk_score, reasons
