from phase1_rule_ids.packet_sniffer import start_sniffing
from phase3_hybrid_ids.ip_blocker import start_unblock_daemon

if __name__ == "__main__":
    start_unblock_daemon()
    start_sniffing()
