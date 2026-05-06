from collections import defaultdict

class TrafficAggregator:
    #tracks per ip: packet count, port assessed, packet sizes, tcp flags
    def __init__(self):
        self.packet_count = defaultdict(int)
        self.total_size = defaultdict(int)
        self.port_set = defaultdict(set)
        self.tcp_flags = defaultdict(int)

    def update(self, packet):
        if not packet.haslayer("IP"):
            return

        src = packet["IP"].src

        self.packet_count[src] += 1
        self.total_size[src] += len(packet)

        if packet.haslayer("TCP"):
            self.port_set[src].add(packet["TCP"].dport)
            self.tcp_flags[src] += int(packet["TCP"].flags)

    def get_features(self, src_ip, window):

        count = self.packet_count[src_ip]

        if count == 0:
            return None

        avg_size = self.total_size[src_ip] / count
        unique_ports = len(self.port_set[src_ip])
        rate = count / window
        flag_sum = self.tcp_flags[src_ip]

        return [
            count,
            rate,
            unique_ports,
            avg_size,
            flag_sum
        ]

    def reset(self):
        self.packet_count.clear()
        self.total_size.clear()
        self.port_set.clear()
        self.tcp_flags.clear()
