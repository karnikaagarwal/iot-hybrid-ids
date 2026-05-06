import paho.mqtt.client as mqtt
import time
import random
import json

BROKER = "10.0.0.3"

client = mqtt.Client("smart_camera")
client.connect(BROKER, 1883)

while True:
    data = {
        "device": "SmartCamera",
        "motion": random.randint(0,1),
        "timestamp": time.time()
    }

    client.publish("home/camera", json.dumps(data))
    print("[Camera] Sent:", data)

    time.sleep(2)
