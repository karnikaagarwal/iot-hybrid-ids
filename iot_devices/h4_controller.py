import paho.mqtt.client as mqtt
import time

BROKER="10.0.0.3"

client=mqtt.Client("controller")
client.connect(BROKER,1883)

while True:
    client.publish("home/control","status_check")
    print("[Controller] Checking devices...")
    time.sleep(5)

