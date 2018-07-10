import RPi.GPIO as GPIO
import urllib.request
import json, datetime, time

button = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

usr = "admin"
pw = "private"
top_level_url = "http://192.168.1.188"
p = urllib.request.HTTPPasswordMgrWithDefaultRealm()
p.add_password(None, top_level_url, usr, pw)
auth_handler = urllib.request.HTTPDigestAuthHandler(p)
opener = urllib.request.build_opener(auth_handler)
open = urllib.request.install_opener(opener)

def forcemode(state):
	if state == "On":
		req = urllib.request.Request('http://192.168.1.188/w/force.lr?cmd=fm&po=0&ch=0&v=1')
		result = opener.open(req)

	if state == "Off":
		req = urllib.request.Request('http://192.168.1.188/w/force.lr?cmd=fm&po=0&ch=0&v=0')
		result = opener.open(req)
	else:
		pass

def activate(port, state):
	if state == "On":
		req = urllib.request.Request('http://192.168.1.188/w/force.lr?cmd=pm&po='+str(port)+'&ch=0&v=4')
		result = opener.open(req)

	if state == "Off":
		req = urllib.request.Request('http://192.168.1.188/w/force.lr?cmd=pm&po='+str(port)+'&ch=0&v=0')
		result = opener.open(req)
	else:
		pass

def trigger():
	if GPIO.input(button) == False:
		return True
	else:
		return False

def request(port):
	data = urllib.request.Request('http://192.168.1.188/r/ioldetails.lr?port='+str(port)+'&_')
	result = opener.open(data)
	data = result.read()
	data = json.loads(data.decode("utf-8"))
	raw = data["iol"]["data"]["input"]
	return raw

def mm(raw):
	ref_one = 25
	ref_two = 255.0

	a = raw[0] * ref_one
	b = raw[1] / ref_two * ref_one
	dist = a + b
	return dist

def present(dist):
	th = 75
	if dist > th:
		return 0
	else:
		return 1

def oneOrZero(port):
	return present(mm(request(port)))

def pubMsg(result, broker):
	topic = "Sensors/RaspberryPi01/PnF"
	timestamp = datetime.today().strftime("%Y-%m-%d %H:$M:%S.%f")[:-3]
	payload = '{"timestamp": "%s", "result": "%s"}' % (timestamp, result)
	return topic, payload, broker
