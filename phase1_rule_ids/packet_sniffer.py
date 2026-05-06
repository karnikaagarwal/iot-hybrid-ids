from phase3_hybrid_ids.shared_state import update_packet_count
from scapy.all import sniff, get_if_list

from phase1_rule_ids.rule_engine import process_packet
from phase2_ml_ids.ml_detector import ml_process_packet


def get_mininet_interfaces():
    interfaces = get_if_list()

    mn_ifaces = [i for i in interfaces if "s1-eth" in i]

    if not mn_ifaces:
        print("⚠ No Mininet interfaces found")
        exit()

    print(f"✅ Monitoring interfaces: {mn_ifaces}")
    return mn_ifaces


def handle_packet(packet):
    #ignore invalid traffic like noises, arp etc .
    if not packet.haslayer("IP"):
        return

    src_ip = packet["IP"].src
    #avoid invalid packets
    if src_ip == "0.0.0.0" or src_ip.startswith("224.") or src_ip.startswith("255"):
        return

    # ✅ update packet count
    update_packet_count()
    
    
   #sent to both ids engines

    # Phase 1
    process_packet(packet)

    # Phase 2
    ml_process_packet(packet)
    
    

def start_sniffing():

    interfaces = get_mininet_interfaces()

    print("🚀 Hybrid IDS Started...")

    sniff(
        iface=interfaces,
        prn=handle_packet,
        store=False
        # packet store in ram -> forever memory usage
    )
