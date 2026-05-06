from scapy.all import sniff
from scapy.layers.inet import IP, TCP
from collections import defaultdict
from scapy.all import get_if_list
import time
import csv

OUTPUT_FILE = "dataset.csv"
WINDOW = 5

print("📡 Aggregated dataset capture started...")

# Create CSV
with open(OUTPUT_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "packet_count",
        "rate",
        "unique_ports",
        "avg_packet_size",
        "tcp_flag_sum",
        "label"
    ])

# Tracking
packet_count = defaultdict(int)
port_access = defaultdict(set)
packet_sizes = defaultdict(list)
tcp_flags = defaultdict(int)

start_time = time.time()


def process_window():
    """Write current window data to CSV"""
    global start_time

    if not packet_count:
        return

    with open(OUTPUT_FILE, "a", newline="") as f:
        writer = csv.writer(f)

        for ip in packet_count:

            count = packet_count[ip]
            rate = count / WINDOW
            unique_ports = len(port_access[ip])
            avg_size = sum(packet_sizes[ip]) / count
            flag_sum = tcp_flags[ip]

            # 🔥 LABEL LOGIC (STABLE)
            if rate > 100:
                label = 2  # DDoS
            elif unique_ports > 10:
                label = 1  # Port scan
            else:
                label = 0  # Normal

            writer.writerow([
                count,
                rate,
                unique_ports,
                avg_size,
                flag_sum,
                label
            ])

    # reset
    packet_count.clear()
    port_access.clear()
    packet_sizes.clear()
    tcp_flags.clear()
    start_time = time.time()


def process_packet(packet):
    global start_time

    if not packet.haslayer(IP):
        return

    src_ip = packet[IP].src

    packet_count[src_ip] += 1
    packet_sizes[src_ip].append(len(packet))

    if packet.haslayer(TCP):
        port_access[src_ip].add(packet[TCP].dport)
        tcp_flags[src_ip] += int(packet[TCP].flags)

    current_time = time.time()

    # 🔥 FORCE WINDOW WRITE
    if current_time - start_time >= WINDOW:
        process_window()

interfaces = [i for i in get_if_list() if "s1-eth" in i]

print("Using interfaces:", interfaces)
# 🔥 START SNIFFING
sniff(
    iface=interfaces,
    prn=process_packet,
    store=0
)
