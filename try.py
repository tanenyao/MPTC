import urllib.request
import json

user = "admin"
pw = "private"

top_level_url = 'http://192.168.1.188'

p = urllib.request.HTTPPasswordMgrWithDefaultRealm()
p.add_password(None, top_level_url, user, pw)

auth_handler = urllib.request.HTTPDigestAuthHandler(p)
opener = urllib.request.build_opener(auth_handler)

urllib.request.install_opener(opener)

try:
	forceon = urllib.request.Request('http://192.168.1.188/w/force.lr?cmd=fm&po=0&ch=0&v=1')	# v: 0-OFF 1-ON
	result = opener.open(forceon)

	x1 = urllib.request.Request('http://192.168.1.188/w/force.lr?cmd=pm&po=0&ch=0&v=4')		# v: 0-Inactive 1-DigitalInput 2-DigitalOutput 3-IO-LinkSIO 4-IO-Link
	result = opener.open(x1)

	x2 = urllib.request.Request('http://192.168.1.188/w/force.lr?cmd=pm&po=1&ch=0&v=4')		# v: 0-Inactive 1-DigitalInput 2-DigitalOutput 3-IO-LinkSIO 4-IO-Link
	result = opener.open(x2)

	while True:
		x1_data = urllib.request.Request('http://192.168.1.188/r/ioldetails.lr?port=0&_')
		result = opener.open(x1_data)
		x1_data = result.read()
		x1_data = json.loads(x1_data.decode("utf-8"))
		x1_read = x1_data["iol"]["data"]["input"]
		print(x1_read)

		x2_data = urllib.request.Request('http://192.168.1.188/r/ioldetails.lr?port=1&_')
		result = opener.open(x2_data)
		x2_data = result.read()
		x2_data = json.loads(x2_data.decode("utf-8"))
		x2_read = x2_data["iol"]["data"]["input"]
		print(x2_read)

		# (mapping function here)

except IOError as e:
	print(e)
