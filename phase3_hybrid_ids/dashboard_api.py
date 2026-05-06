from flask import Flask, jsonify, request, send_from_directory

from flask_socketio import SocketIO
import time
import json

from phase3_hybrid_ids.shared_state import read_stats, read_alerts, read_live_alerts
from phase3_hybrid_ids.ip_blocker import block_ip, unblock_ip

BLOCK_FILE = "/home/ubuntu-iot-hub/iot-hybrid-ids/phase3_hybrid_ids/blocked_ips.json"

def read_blocked():
    try:
        with open(BLOCK_FILE, "r") as f:
            return json.load(f)
    except:
        return {}



app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

def push_update(event, data):
    socketio.emit(event, data)

# HOME
@app.route("/")
def home():
    return send_from_directory("static", "index.html")


# STATS
@app.route("/stats")
def get_stats():
    stats = read_stats()
    blocked = read_blocked()

    return jsonify({
        "total_packets": stats["total_packets"],
        "alerts": len(read_live_alerts()),
        "blocked": len(blocked)
    })


# ALERTS (LAST 10 SECONDS ONLY)
@app.route("/alerts")
def get_alerts():
    return jsonify(read_live_alerts())


# BLOCKED IPS (FIXED)
@app.route("/blocked")
def get_blocked():

    blocked = read_blocked()

    # 🔥 CORRECT DEBUG
    print("BLOCKED IPS FILE:", blocked)

    data = []

    for ip, t in blocked.items():
        remaining = int(120 - (time.time() - t))

        data.append({
            "ip": ip,
            "time_left": max(0, remaining)
        })

    return jsonify(data)


# MANUAL BLOCK
@app.route("/block_manual", methods=["POST"])
def manual_block():
    ip = request.json.get("ip")
    block_ip(ip)
    return {"status": "blocked"}


# MANUAL UNBLOCK
@app.route("/unblock", methods=["POST"])
def unblock_ip_api():
    ip = request.json.get("ip")
    unblock_ip(ip)
    return {"status": "unblocked"}


# DOWNLOAD LOGS
@app.route("/download_logs")
def download_logs():
    return send_from_directory(
        "/home/ubuntu-iot-hub/iot-hybrid-ids/",
        "alerts.log",
        as_attachment=True
    )


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
