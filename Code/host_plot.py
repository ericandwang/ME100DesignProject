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

# mqtt callbacks
def data(c, u, message):
    # extract data from MQTT message
    msg = message.payload.decode('ascii')
    # convert to vector of floats
    f = [ float(x) for x in msg.split(',') ]
    print("received", f)
    # append to data vectors, add more as needed
    t.append(f[0])
    s.append(f[1])

def plot(client, userdata, message):
    # customize this to match your data
    print("plotting ...")
    plt.plot(t, s, 'rs')
    plt.xlabel('Time')
    plt.ylabel('Sinusoid')
    print("show plot ...")
    # show plot on screen
    plt.show()

# subscribe to topics
data_topic = "{}/data".format(session, qos)
plot_topic = "{}/plot".format(session, qos)
mqtt.subscribe(data_topic)
mqtt.subscribe(plot_topic)
mqtt.message_callback_add(data_topic, data)
mqtt.message_callback_add(plot_topic, plot)

# wait for MQTT messages
# this function never returns
print("waiting for data ...")
mqtt.loop_forever()
