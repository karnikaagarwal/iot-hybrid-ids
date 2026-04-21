from packet_capture import capture_packets
from rule_engine import process_packet

print("Starting Advanced Rule-Based IDS...")

capture_packets(process_packet)

