def calculate_threat(ml_confidence, rule_hit):

    score = ml_confidence * 70

    if rule_hit:
        score += 30

    return min(score,100)
