import csv
import os

LOG_FILE = "../logs/rule_alerts.csv"

def log_alert(features, alerts):

    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["timestamp","src_ip","packet_rate","alert"])

        for alert in alerts:
            writer.writerow([
                features["timestamp"],
                features["src_ip"],
                features["packet_rate"],
                alert
            ])
