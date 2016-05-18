import RPi.GPIO as gpio
import paho.mqtt.client as mqtt
import time
import dht11
import datetime

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.cleanup()
instance = dht11.DHT11(pin = 5)

while True:
	result = instance.read()
	mqttc = mqtt.Client("python_pub")
       	mqttc.connect("test.mosquitto.org", 1883)
        mqttc.publish("environment/temperature", result.temperature)
        print ("Temperature : %dC" % result.temperature)
        
        time.sleep(1)
mqttc.loop(0)

