import joblib
import time
import pandas as pd
from scapy.layers.inet import IP

from phase1_rule_ids.alert_logger import log_alert
from phase1_rule_ids.alert_formatter import format_alert
from phase2_ml_ids.feature_aggregator import TrafficAggregator
from phase3_hybrid_ids.ip_blocker import register_alert

aggregator = TrafficAggregator()

# 🔥 FIX: safe model loading
try:
    model = joblib.load("/home/ubuntu-iot-hub/iot-hybrid-ids/phase2_ml_ids/model.pkl")
except:
    print("⚠ ML model not found, ML disabled")
    model = None

start_time = time.time()
WINDOW = 5


def ml_process_packet(packet):
    global start_time

    if model is None:
        return

    if not packet.haslayer(IP):
        return

    aggregator.update(packet)

    current_time = time.time()

    if current_time - start_time >= WINDOW:

        for ip in list(aggregator.packet_count.keys()):

            features = aggregator.get_features(ip, WINDOW)

            if features is None or len(features) != 5:
                continue

            try:
                columns = [
                    "packet_count",
                    "rate",
                    "unique_ports",
                    "avg_packet_size",
                    "tcp_flag_sum"
                ]

                df = pd.DataFrame([features], columns=columns)

                prediction = model.predict(df)[0]

                if prediction == 2:
                    attack = "DDoS Attack"
                elif prediction == 1:
                    attack = "Port Scan"
                else:
                    continue

                alert = format_alert(
                    alert_type=attack,
                    severity="HIGH",
                    sources=[ip],
                    packet_count=int(features[0]),
                    window=WINDOW,
                    extra="ML behavior analysis"
                )

                log_alert(alert)
                register_alert(ip)

            except Exception as e:
                print("ML error:", e)

        aggregator.reset()
        start_time = current_time
