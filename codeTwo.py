'''--------------------------------------------------
		HARDWARE SETUP

Pin 15,18,23	Pepperl+Fuchs OMT150 "Detect"
Pin 14		Pepperl+Fuchs OMT150 "Trigger"


--------------------------------------------------'''

import RPi.GPIO as GPIO
import time

delay1=0.1
delay2=0.2
delay3=1

l=[]
c=0
b=0

GPIO.setmode(GPIO.BCM)

GPIO.setup(14, GPIO.IN)
GPIO.setup(15, GPIO.IN)
GPIO.setup(18, GPIO.IN)
GPIO.setup(23, GPIO.IN)

'''while True:
	print(GPIO.input(14))
	print(GPIO.input(15))
	print(GPIO.input(18))
	print(GPIO.input(23))
'''

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
			l=[]
			c=0
			print(' ')
			time.sleep(delay3)

	if GPIO.input(14)==1 and b==1:
		time.sleep(delay1)
		b=0
