from collections import deque

# 🔥 Live shared data (used by IDS + Dashboard)

stats = {
    "total_packets": 0,
    "alerts": 0,
}

# keep last 100 alerts
alerts = deque(maxlen=100)

