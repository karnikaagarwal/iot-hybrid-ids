from scapy.layers.inet import IP, TCP

def extract_features(packet):

    features = {
        "src_ip": None,
        "dst_ip": None,
        "packet_size": 0,
        "tcp_flags": 0
    }

    if packet.haslayer(IP):
        features["src_ip"] = packet[IP].src
        features["dst_ip"] = packet[IP].dst
        features["packet_size"] = len(packet)

    if packet.haslayer(TCP):
        features["tcp_flags"] = packet[TCP].flags

    return features
