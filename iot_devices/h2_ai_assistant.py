import paho.mqtt.client as mqtt
import time
import random
import json

BROKER = "10.0.0.3"

client = mqtt.Client("ai_assistant")
client.connect(BROKER,1883)

commands = ["lights_on","lights_off","music_play","idle"]

while True:
    data = {
        "device":"AIAssistant",
        "command":random.choice(commands),
        "timestamp":time.time()
    }

    client.publish("home/assistant", json.dumps(data))
    print("[Assistant] Sent:", data)

    time.sleep(3)
