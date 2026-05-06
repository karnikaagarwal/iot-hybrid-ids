import os
import time
import json
import threading
from collections import defaultdict

BASE = "/home/ubuntu-iot-hub/iot-hybrid-ids/phase3_hybrid_ids/"
BLOCK_FILE = BASE + "blocked_ips.json"

alert_counter = defaultdict(int)
blocked_ips = {}

ALERT_THRESHOLD = 3
BLOCK_TIME = 120


#  LOAD BLOCKS FROM FILE
def load_blocks():
    global blocked_ips
    try:
        with open(BLOCK_FILE, "r") as f:
            blocked_ips.update(json.load(f))
    except:
        blocked_ips = {}


#  SAFE SAVE (NO CORRUPTION)
def save_blocks():
    temp_file = BLOCK_FILE + ".tmp"

    with open(temp_file, "w") as f:
        json.dump(blocked_ips, f)

    os.replace(temp_file, BLOCK_FILE)


#  ALERT TRACKING
def register_alert(ip):
    alert_counter[ip] += 1
    print(f"[ALERT COUNT] {ip} -> {alert_counter[ip]}")

    if alert_counter[ip] >= ALERT_THRESHOLD:
        block_ip(ip)


#  BLOCK IP
def block_ip(ip):

    if ip in blocked_ips:
        return

    print(f"⛔ BLOCKING IP: {ip}")

    os.system(f"sudo iptables -A INPUT -s {ip} -j DROP")

    blocked_ips[ip] = time.time()
    save_blocks()


#  UNBLOCK IP (FIXED)
def unblock_ip(ip):

    if ip not in blocked_ips:
        return

    print(f"✅ UNBLOCKING IP: {ip}")

    # 🔥 FIX: avoid error spam
    os.system(f"sudo iptables -D INPUT -s {ip} -j DROP 2>/dev/null")

    del blocked_ips[ip]
    alert_counter[ip] = 0
    save_blocks()


#  AUTO UNBLOCK
def unblock_ips():
    current_time = time.time()

    for ip, block_time in list(blocked_ips.items()):
        # main firewall rule
        if current_time - block_time > BLOCK_TIME:
            unblock_ip(ip)


#  BACKGROUND THREAD
def unblock_daemon():
    while True:
        unblock_ips()
        time.sleep(5)   # every 5 sec check blocked ips remove expired blocks


#  START SYSTEM
def start_unblock_daemon():
    load_blocks()

    # IMPORTANT: sync iptables with file
    os.system("sudo iptables -F")

    t = threading.Thread(target=unblock_daemon, daemon=True)
    t.start()
