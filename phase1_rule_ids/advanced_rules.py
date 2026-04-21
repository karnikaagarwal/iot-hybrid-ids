RULES = {
    "PORT_SCAN_RATE": 50,
    "DOS_PACKET_RATE": 200,
    "SUSPICIOUS_RATE": 100
}

def evaluate_rules(features):

    alerts = []

    if features["packet_rate"] > RULES["DOS_PACKET_RATE"]:
        alerts.append("DOS_ATTACK")

    elif features["packet_rate"] > RULES["PORT_SCAN_RATE"]:
        alerts.append("PORT_SCAN")

    elif features["packet_rate"] > RULES["SUSPICIOUS_RATE"]:
        alerts.append("TRAFFIC_ANOMALY")

    return alerts
