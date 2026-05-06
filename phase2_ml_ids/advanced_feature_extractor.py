# advanced_feature_extractor.py

import time
from collections import defaultdict
import numpy as np

flow_data = defaultdict(list)

def update_flow(src_ip, pkt_len, dst_port):

    flow_data[src_ip].append({
        "time": time.time(),
        "size": pkt_len,
        "port": dst_port
    })

def extract_features(src_ip):

    packets = flow_data[src_ip]

    if len(packets) < 5:
        return None

    sizes = [p["size"] for p in packets]
    ports = [p["port"] for p in packets]

    duration = packets[-1]["time"] - packets[0]["time"]

    features = [
        len(packets),                        # packet_count
        len(set(ports)),                    # unique_ports
        np.mean(sizes),                     # mean_size
        np.std(sizes),                      # std_size
        len(packets)/max(duration,1)        # packet_rate
    ]

    return features
