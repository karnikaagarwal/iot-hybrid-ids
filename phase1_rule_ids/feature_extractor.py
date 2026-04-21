import time

flow_table = {}

def extract_features(pkt):

    try:
        src = pkt[0][1].src
    except:
        src = "unknown"

    now = time.time()

    if src not in flow_table:
        flow_table[src] = {
            "count": 0,
            "start": now
        }

    flow_table[src]["count"] += 1

    duration = now - flow_table[src]["start"]

    rate = flow_table[src]["count"] / (duration + 0.01)

    return {
        "src_ip": src,
        "packet_rate": rate,
        "timestamp": now
    }
