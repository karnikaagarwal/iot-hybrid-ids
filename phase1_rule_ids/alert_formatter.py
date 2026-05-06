from datetime import datetime

def format_alert(alert_type, severity, sources, packet_count, window, extra=""):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    alert = f"""
🚨 ================= IDS ALERT =================
Time        : {timestamp}
Attack Type : {alert_type}
Severity    : {severity}
Sources     : {', '.join(sources) if isinstance(sources, list) else sources}
Packets     : {packet_count} in {window}s
Details     : {extra}
================================================
"""

    return alert
