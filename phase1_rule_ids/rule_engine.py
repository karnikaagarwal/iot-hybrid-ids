import time
from collections import defaultdict

from phase1_rule_ids.alert_logger import log_alert
from phase1_rule_ids.alert_formatter import format_alert
from phase1_rule_ids.config import (
    PACKET_RATE_THRESHOLD,
    TIME_WINDOW,
    UNIQUE_IP_THRESHOLD
)

from phase3_hybrid_ids.ip_blocker import register_alert, unblock_ips

packet_count = defaultdict(int)
start_time = time.time()

# analyse packet behaviour using threshold/rules
def process_packet(packet):

    global start_time, packet_count

    if not packet.haslayer("IP"):
        return

    #extract source_ip
    src_ip = packet["IP"].src
    #count traffic
    packet_count[src_ip] += 1

    #Every 5 seconds: evaluate traffic.
    current_time = time.time()

    #  FIX: always check unblock (not only inside window)
    unblock_ips()

    if current_time - start_time >= TIME_WINDOW:

        total_packets = sum(packet_count.values())
        sources = list(packet_count.keys())

        #  RULE 1 — DDoS
        if total_packets > PACKET_RATE_THRESHOLD:

            alert = format_alert(
                alert_type="DDoS / Traffic Flood",
                severity="HIGH",
                sources=sources,
                packet_count=total_packets,
                window=TIME_WINDOW,
                extra="Traffic threshold exceeded"
            )

            log_alert(alert)

            top_ips = sorted(
                packet_count.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]

            for ip, _ in top_ips:
                 register_alert(ip)
                 
        #  RULE 2 — Single IP Flood
        for ip, count in packet_count.items():

            if count > PACKET_RATE_THRESHOLD:

                alert = format_alert(
                    alert_type="Single-IP Flood Attack",
                    severity="HIGH",
                    sources=[ip],
                    packet_count=count,
                    window=TIME_WINDOW,
                    extra="One IP dominating traffic"
                )

                log_alert(alert)
                register_alert(ip)

        #  RULE 3 — Bot Activity
        if len(packet_count) > UNIQUE_IP_THRESHOLD:

            alert = format_alert(
                alert_type="Distributed Bot-like Activity",
                severity="MEDIUM",
                sources=sources,
                packet_count=total_packets,
                window=TIME_WINDOW,
                extra="Too many unique IPs"
            )

            log_alert(alert)

            top_ips = sorted(
                packet_count.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]

            for ip, _ in top_ips:
                register_alert(ip)

        packet_count.clear()
        start_time = current_time
