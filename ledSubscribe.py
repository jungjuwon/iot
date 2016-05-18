import paho.mqtt.client as mqtt
import RPi.GPIO as gpio
import time
import datetime

gpio.setwarnings(False)

ledg_pin = 6
ledy_pin = 20
ledr_pin = 12

gpio.setmode(gpio.BCM)
gpio.setup(ledg_pin, gpio.OUT)
gpio.setup(ledy_pin, gpio.OUT)
gpio.setup(ledr_pin, gpio.OUT)

tem = 0
dis = 0

temMsg = 0
disMsg = 0

temChk = 0
disChk = 0

preTem = 0
def on_connect(client, userdata, rc):
    print("Connected with result coe " + str(rc))
    client.subscribe("environment/temperature")
    client.subscribe("environment/ultrasonic")

def on_message(client, userdata, msg):

    global tem, dis, temMsg, disMsg, temChk, disChk, preTem

    if(msg.topic == "environment/temperature"):
        tem = float(msg.payload)
        temMsg = str(msg.topic)
        temChk = 1
    elif(msg.topic == "environment/ultrasonic"):
        dis = float(msg.payload)
        disMsg = str(msg.topic)
        disChk = 1

    if temChk == 1 and disChk == 1:
	if tem != 0:
		preTem = tem
		if tem < 40:
			print temMsg + " : " +  str(tem) + "		 | " + disMsg + " : " + str(dis)
			if dis >= 100:
				gpio.output(ledg_pin, True)
			elif dis < 100 and dis > 30:
				gpio.output(ledy_pin, True)
			else:
				gpio.output(ledr_pin, True)
		else:
			print "Temperature is too high to operatre Distance Sensor and LED"
	else:
		if preTem == 0:
			print "No Data, No Publish"
		else:
			if preTem < 40:
				print temMsg + " : " +  str(preTem) + "(pre)	 | " + disMsg + " : " + str(dis)
                        	if dis >= 100:
                                	gpio.output(ledg_pin, True)
                        	elif dis < 100 and dis > 30:
                                	gpio.output(ledy_pin, True)
                        	else:
                                	gpio.output(ledr_pin, True)
			else:
				print "Temperature is too high to operatre Distance Sensor and LED"
	time.sleep(1)
	gpio.output(ledg_pin, False)
        gpio.output(ledy_pin, False)
        gpio.output(ledr_pin, False)

        temChk = 0
	disChk = 0

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)
client.loop_forever()

