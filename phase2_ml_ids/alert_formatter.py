from datetime import datetime

def format_alert(alert_type, source, packets, severity):

    return f"""
🚨 ATTACK DETECTED
-----------------------------
Type     : {alert_type}
Source   : {source}
Packets  : {packets}
Severity : {severity}
Time     : {datetime.now()}
-----------------------------
"""
