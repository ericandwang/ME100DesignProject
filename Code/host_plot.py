import paho.mqtt.client as paho
import matplotlib.pyplot as plt

# MQTT parameters
session = "EricWang/ESP32/measurements"
BROKER = 'broker.mqttdashboard.com'
qos = 0

# connect to MQTT broker
print("Connecting to MQTT broker", BROKER, "...", end="")
mqtt = paho.Client()
mqtt.connect(BROKER, port=1883)
print("Connected!")

# initialize data vectors
# in this example we plot only 1 value, add more as needed
t = []
s = []

# initialize popup boolean
canPop = 1

# mqtt callbacks
def data(c, u, message):
    global canPop
    # extract data from MQTT message
    msg = message.payload.decode('ascii')
    # convert to vector of floats
    f = [ float(x) for x in msg.split(',') ]
    print("received", f)
    # append to data vectors, add more as needed
    t.append(f[0])
    s.append(f[1])
    if (f[1] < 20 and canPop == 1):
        topic = "{}/popup".format(session)
        data = "do popup"
        mqtt.publish(topic, data)
        canPop = 0


def releasePopup(client, userdata, message):
    global canPop
    msg = message.payload.decode('ascii')
    if (msg == "popup released"):
        canPop = 1
    print(msg)

# subscribe to topics
data_topic = "{}/data".format(session, qos)
mqtt.subscribe(data_topic)
mqtt.message_callback_add(data_topic, data)

popup_topic = "{}/popup".format(session, qos)
mqtt.subscribe(popup_topic)
mqtt.message_callback_add(popup_topic, releasePopup)

# wait for MQTT messages
# this function never returns
print("waiting for data ...")
mqtt.loop_forever()
