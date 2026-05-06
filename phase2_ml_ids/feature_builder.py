from scapy.layers.inet import IP, TCP, UDP

def extract_ml_features(packet):

    features = {
        "packet_size": 0,
        "proto": 0,
        "tcp_flags": 0,
        "src_port": 0,
        "dst_port": 0
    }

    if packet.haslayer(IP):
        features["packet_size"] = len(packet)

    if packet.haslayer(TCP):
        features["proto"] = 1
        features["tcp_flags"] = int(packet[TCP].flags)
        features["src_port"] = packet[TCP].sport
        features["dst_port"] = packet[TCP].dport

    elif packet.haslayer(UDP):
        features["proto"] = 2
        features["src_port"] = packet[UDP].sport
        features["dst_port"] = packet[UDP].dport

    return list(features.values())
