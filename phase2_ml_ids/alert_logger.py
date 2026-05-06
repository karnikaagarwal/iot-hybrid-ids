from datetime import datetime
from phase3_hybrid_ids.shared_state import update_alert

LOG_FILE = "/home/ubuntu-iot-hub/iot-hybrid-ids/logs/alerts.log"

def log_alert(alert):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    full_alert = f"""
🚨 ================= IDS ALERT =================
Time        : {timestamp}
{alert}
================================================
"""

    print(full_alert)

    with open(LOG_FILE, "a") as f:
        f.write(full_alert + "\n")

    # 🔥 THIS FIXES EVERYTHING
    update_alert(full_alert)
