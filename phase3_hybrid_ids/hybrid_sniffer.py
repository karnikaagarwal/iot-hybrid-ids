import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scapy.all import sniff
from scapy.layers.inet import IP, TCP

from phase1_rule_ids.rule_engine import process_packet as rule_process
from phase2_ml_ids.ml_detector import ml_process_packet
from phase3_hybrid_ids.fusion_engine import FusionEngine

engine = FusionEngine()

print("🚀 Hybrid IDS started...")

def handle_packet(packet):
    try:
        # Phase 1 (Rule)
        rule_result = rule_process(packet)

        # Phase 2 (ML)
        ml_result = ml_process_packet(packet)

        # If ML returned None → ignore
        if ml_result is None:
            return

        # Fusion
        final = engine.fuse(
            "ATTACK" if rule_result else "NORMAL",
            {"score": 1.0 if ml_result != "normal" else 0.0}
        )

        # 🔥 Only print if attack
        if final["decision"] == "ATTACK":
            print("\n🔥 HYBRID ALERT 🔥")
            print({
                "decision": final["decision"],
                "confidence": round(final["confidence"], 2),
                "attack_type": ml_result
            })

    except Exception as e:
        print("Hybrid error:", e)


# 🔥 REAL TRAFFIC CAPTURE
sniff(
    filter="tcp port 1883",
    prn=handle_packet,
    store=0
)
