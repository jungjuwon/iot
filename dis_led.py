import RPi.GPIO as gpio
import time
import dht11
import datetime

gpio.setwarnings(False)
trig_pin = 13
echo_pin = 19

ledg_pin = 6
ledy_pin = 20
ledr_pin = 12

gpio.setmode(gpio.BCM)
gpio.setup(trig_pin, gpio.OUT)
gpio.setup(echo_pin, gpio.IN)

gpio.setmode(gpio.BCM)
gpio.setup(ledg_pin, gpio.OUT)
gpio.setup(ledy_pin, gpio.OUT)
gpio.setup(ledr_pin, gpio.OUT)

instance = dht11.DHT11(pin = 5)

preTem = 0
try :        
	while True:
		result = instance.read()

                gpio.output(trig_pin, False)
		gpio.output(ledg_pin, False)
		gpio.output(ledy_pin, False)
		gpio.output(ledr_pin, False)
		time.sleep(0.5)

                gpio.output(trig_pin, True)
                time.sleep(0.00001)

                gpio.output(trig_pin, False)

                while gpio.input(echo_pin) == 0:
                        pulse_start = time.time()

                while gpio.input(echo_pin) == 1:
                        pulse_end = time.time()

                pulse_duration = pulse_end - pulse_start
                distance = pulse_duration * 17000
                distance = round(distance, 2)
			
		if result.temperature < 40:
			if distance >= 100:
				gpio.output(ledg_pin, True)
			elif distance < 100 and distance > 30:
				gpio.output(ledy_pin, True)
			else:
				gpio.output(ledr_pin, True)
			
			if result.temperature != 0:	
				preTem = result.temperature
                		print "Distance : ", distance, "cm"
				print ("Temperature : %dC" % result.temperature)
			else:
				print "Distance : ", distance, "cm"
				print ("Temperature : %dC" % preTem)
		else:
			print "Temperature is too high"

		time.sleep(0.5)
		gpio.output(ledg_pin, False)
                gpio.output(ledy_pin, False)
                gpio.output(ledr_pin, False)
except KeyboardInterrupt:
        gpio.cleanup()
