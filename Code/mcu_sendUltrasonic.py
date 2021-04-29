from mqttclient import MQTTClient
from math import sin
from machine import Pin, PWM, Timer
import time
import network
import sys
from hcsr04 import HCSR04
from machine import Pin,I2C
import gc

# MQTT parameters
session = 'EricWang/ESP32/measurements'
BROKER = 'broker.mqttdashboard.com'

# initialize ultrasonic sensor
sensor = HCSR04(trigger_pin=22, echo_pin=23,echo_timeout_us=1000000)

# check wifi connection
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
ip = wlan.ifconfig()[0]
if ip == '0.0.0.0':
    print("no wifi connection")
    sys.exit()
else:
    print("connected to WiFi at IP", ip)

# connect to MQTT broker
print("Connecting to MQTT broker", BROKER, "...", end="")
mqtt = MQTTClient(BROKER, port=1883)
print("Connected!")

# timer callback function
def tcb(timer):
    t = time.time()
    distance = sensor.distance_cm()
    topic = "{}/data".format(session)
    data = "{},{}".format(t, distance)
    print("send topic='{}' data='{}'".format(topic, data))
    mqtt.publish(topic, data)
    
def cleanup(timer):
    gc.collect()
    gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())

# initialize timer
t1 = Timer(1)
t2 = Timer(2)

# setup timer interrupt
t1.init(period=100, mode=t1.PERIODIC, callback=tcb)
t2.init(period=1000, mode=t2.PERIODIC, callback=cleanup)

# do the plotting (on host)
#print("tell host to do the plotting ...")
#mqtt.publish("{}/plot".format(session), "create the plot")