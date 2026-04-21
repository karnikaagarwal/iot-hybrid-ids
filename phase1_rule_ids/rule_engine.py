from feature_extractor import extract_features
from advanced_rules import evaluate_rules
from alert_logger import log_alert

def process_packet(pkt):

    features = extract_features(pkt)

    alerts = evaluate_rules(features)

    if alerts:
        print("ALERT:", alerts)
        log_alert(features, alerts)
