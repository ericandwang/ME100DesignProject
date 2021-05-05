# imports
import paho.mqtt.client as paho
import matplotlib.pyplot as plt
import numpy as np
import csv

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
t = []
s = []

# initialize popup boolean
canPop = 1
distEst = -1

# filename for csv writing
filename = "postureData.csv"

# mqtt callbacks
def data(c, u, message):
    global canPop
    global distEst
    # extract data from MQTT message
    msg = message.payload.decode('ascii')
    # convert to vector of floats
    f = [ float(x) for x in msg.split(',') ]
    print("received", f)
    # append to data vectors, add more as needed
    if (f[1] <= 1000):
        t.append(f[0])
        s.append(f[1])
        if (len(s) >= 10 and distEst < 0):
            distEst = np.mean(s)
            # writing to csv file for the first time
            with open(filename, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([f[0], distEst])
        elif (distEst >= 0):
            # mean filter with 10 index window
            distEst = np.mean(s[-10:])
            # appending to csv file
            with open(filename, 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([f[0], distEst])
    # popup triggering
    if (distEst <= 30 and distEst >= 0 and canPop == 1):
        topic = "{}/popup".format(session)
        data = "do popup"
        mqtt.publish(topic, data)
        canPop = 0

# callback to release popup
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
