# don't forget the mqtt element

import urllib.request
from func import *

row = 1
col = 3
tot = col*row
l = []

try:
	forcemode("On")
	activate(0,"On")
	activate(1,"On")
	activate(2,"On")

	while True:
		if trigger():
			for i in range(col):
				l.append(oneOrZero(i))

		if len(l) == tot:
			print(l)
			l =[]

except AttributeError:
	GPIO.cleanup()
	print("exit")
