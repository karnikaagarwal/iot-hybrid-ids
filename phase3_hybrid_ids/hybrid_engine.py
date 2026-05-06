def hybrid_decision(rule_alert, ml_result):

    if rule_alert:
        return "BLOCK"

    if ml_result["confidence"] > 0.85:
        return "BLOCK"

    if ml_result["confidence"] > 0.60:
        return "MONITOR"

    return "ALLOW"
