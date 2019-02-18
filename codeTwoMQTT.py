'''--------------------------------------------------
		HARDWARE SETUP

Pin 15,18,23	Pepperl+Fuchs OMT150 "Detect"
Pin 14		Pepperl+Fuchs OMT150 "Trigger"

		WHAT THIS SCRIPT DOES
Programs Pepperl+Fuchs sensors to detect tray pieces
at the MPTC oven machine.

Returns a list of 0s & 1s; 1s representing absence.

List has 12 elements which represents the 12 pieces
on the tray. First 3 elements being the pieces on the
first row, second 3 for the second row, and so on.

MQTT message sent out is in JSON format that includes
the list of 0s & 1s, a timestamp and a 'dummy' trayId.

--------------------------------------------------'''

import RPi.GPIO as GPIO
import time
import paho.mqtt.publish as publish
from datetime import datetime

delay1=0.1
delay2=0.2
delay3=1

l=[]
c=0
b=0

localhost = '172.20.115.20'
topic = 'mptc/oven'
payload = ''

GPIO.setmode(GPIO.BCM)

GPIO.setup(14, GPIO.IN)
GPIO.setup(15, GPIO.IN)
GPIO.setup(18, GPIO.IN)
GPIO.setup(23, GPIO.IN)

while True:
	if GPIO.input(14)==0 and b==0:
		b=1
		time.sleep(delay1)

		if c!=0 and c!=5:
			c+=1
			l.append(GPIO.input(15))
			l.append(GPIO.input(18))
			l.append(GPIO.input(23))
			print(l)
			time.sleep(delay2)
		if c==0:
			c+=1
			print('Start')
		if c==5:
			timestamp = datetime.today().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
			payload = '{"result": "%s", "timestamp": "%s", trayId: "1"}' % (str(l),timestamp)
			publish.single(topic, payload, qos=2, retain=False,
			hostname=localhost, port=1883, client_id="",
			keepalive=60, will=None, auth=None, tls=None)
			print("Message Published Successfully")

			l=[]
			c=0
			print(' ')
			time.sleep(delay3)

	if GPIO.input(14)==1 and b==1:
		time.sleep(delay1)
		b=0
