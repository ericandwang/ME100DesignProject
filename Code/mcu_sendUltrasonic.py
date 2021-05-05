# imports
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
qos = 0

# initialize ultrasonic sensor
sensor = HCSR04(trigger_pin=22, echo_pin=23,echo_timeout_us=1000000)

# initialize LED pin and PWM
led_ext1 = Pin(16, mode=Pin.OUT)
led_ext2 = Pin(17, mode=Pin.OUT)
led_ext3 = Pin(21, mode=Pin.OUT)
L1 = PWM(led_ext1,freq=200,duty=0,timer=0)
L2 = PWM(led_ext2,freq=200,duty=0,timer=0)
L3 = PWM(led_ext3,freq=200,duty=0,timer=0)

# initialize global variables
blinker = 0
distance = 10000

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
    global distance
    t = time.time()
    distance = sensor.distance_cm()
    topic = "{}/data".format(session)
    data = "{},{}".format(t, distance)
    print("send topic='{}' data='{}'".format(topic, data))
    mqtt.publish(topic, data)

# memory cleanup callback function
def cleanup(timer):
    gc.collect()
    gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())

# periodic blinking callback function
def blink(timer):
    global blinker
    if (blinker):
        L1.duty(80)
    else:
        L1.duty(0)
    blinker = not blinker

# initialize timer
t1 = Timer(1)
t2 = Timer(2)
t3 = Timer(3)

# setup timer interrupt
t1.init(period=100, mode=t1.PERIODIC, callback=tcb)
t2.init(period=1000, mode=t2.PERIODIC, callback=cleanup)
t3.init(period=50, mode=t3.PERIODIC, callback=blink)

# main loop for toggling warning LEDs
while True:
    if (distance <= 30):
        L2.duty(100)
        L3.duty(100)
    else:
        L2.duty(0)
        L3.duty(0)