import json
import os

BASE = "/home/ubuntu-iot-hub/iot-hybrid-ids/phase3_hybrid_ids/"

STATS_FILE = BASE + "stats.json"
ALERT_FILE = BASE + "alerts.json"

LIVE_ALERT_FILE = BASE + "live_alerts.json"

def init_files():
    if not os.path.exists(STATS_FILE):
        with open(STATS_FILE, "w") as f:
            json.dump({"total_packets": 0, "alerts": 0}, f)

    if not os.path.exists(ALERT_FILE):
        with open(ALERT_FILE, "w") as f:
            json.dump([], f)

    #ALWAYS RESET LIVE ALERTS
    with open(LIVE_ALERT_FILE, "w") as f:
        json.dump([], f)

def update_packet_count():
    data = read_stats()
    data["total_packets"] += 1
    write_stats(data)


def update_alert(alert):
    data = read_stats()
    data["alerts"] += 1
    write_stats(data)

    # ---------- MAIN LOG ----------
    alerts = read_alerts()
    alerts.append(alert)
    alerts = alerts[-100:]

    with open(ALERT_FILE, "w") as f:
        json.dump(alerts, f)

    # ---------- LIVE ALERTS ----------
    try:
        with open(LIVE_ALERT_FILE) as f:
            live = json.load(f)
    except:
        live = []

    live.append(alert)
    live = live[-20:]  # only last 20 live alerts

    with open(LIVE_ALERT_FILE, "w") as f:
        json.dump(live, f)
        
        

def read_stats():
    with open(STATS_FILE) as f:
        return json.load(f)


def write_stats(data):
    with open(STATS_FILE, "w") as f:
        json.dump(data, f)


def read_alerts():
    with open(ALERT_FILE) as f:
        return json.load(f)
        
def read_live_alerts():
    try:
        with open(LIVE_ALERT_FILE) as f:
            return json.load(f)
    except:
        return []
