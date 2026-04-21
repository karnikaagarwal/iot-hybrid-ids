from scapy.all import sniff

def capture_packets(callback):
    sniff(
        iface="eth0",
        prn=callback,
        store=False
    )
