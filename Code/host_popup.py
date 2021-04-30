import paho.mqtt.client as paho
import matplotlib.pyplot as plt
import ctypes

# MQTT parameters
session = "EricWang/ESP32/measurements"
BROKER = 'broker.mqttdashboard.com'
qos = 0

# connect to MQTT broker
print("Connecting to MQTT broker", BROKER, "...", end="")
mqtt = paho.Client()
mqtt.connect(BROKER, port=1883)
print("Connected!")

# mqtt callbacks
def doPopup(c, u, message):
    msg = message.payload.decode('ascii')
    if (msg == "do popup"):
        ctypes.windll.user32.MessageBoxW(0, "Straighten Back Please", "Posture Alert", 0)
        topic = "{}/popup".format(session)
        data = "popup released"
        mqtt.publish(topic, data)

# subscribe to topics
popup_topic = "{}/popup".format(session, qos)
mqtt.subscribe(popup_topic)
mqtt.message_callback_add(popup_topic, doPopup)

# wait for MQTT messages
# this function never returns
print("waiting for data ...")
mqtt.loop_forever()
