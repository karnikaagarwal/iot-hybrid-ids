import paho.mqtt.client as mqtt

BROKER="10.0.0.3"

def on_message(client, userdata, msg):
    print(f"[DoorLock] {msg.topic} -> {msg.payload.decode()}")

client = mqtt.Client("smart_lock")

client.on_message = on_message
client.connect(BROKER,1883)

client.subscribe("#")
client.loop_forever()
