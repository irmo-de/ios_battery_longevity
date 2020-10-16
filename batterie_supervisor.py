#!usr/bin/python

import urllib.request
import ssl
import time
import subprocess
import re

# import datetime


# constant values


# f = open("/irmo/log.txt", "at")

# f.write("%s" % datetime.datetime.now())

# quit()

DATA_ON  = b'{"on":true}'
DATA_OFF = b'{"on":false}'

url='https://philips-hue.fritz.box/api/zHOKjohzHiPvlH2NU0uGlChh-GbWL-73iYQdw2er/lights/12/state'

regex_cap = rb'"CurrentCapacity" = (\d+)'
regex_charge = rb'"IsCharging" = (\w+)'

limit_lower = 67 # start charging if below or equal this value
limit_upper = 70 # stop charging if above or equal this value

#time_to_sleep = 60 # wake up every x seconds to check battery status


def isCharging(regex_charge, result):
	# are we charging?
	# Lets look if device is charging / remember every wifi call is expensive in terms of power consumption

	match = re.search(regex_charge, result.stdout)  

	if (match != None):
		charging = match.group(1) == b'Yes'
	else:
		charging = False

	print (charging)

	return charging


while (True):

	# Getting battery level

	result = subprocess.run(['ioreg', '-w0','-p', 'IOPower', '-c', 'AppleARMPMUCharger', '-r'], stdout=subprocess.PIPE)
	match = re.search(regex_cap, result.stdout)  

	if (match != None):
		battery_level = int(match.group(1))
	else:
		battery_level = 100

	print (battery_level)




	if (battery_level <= limit_lower):
		print ("Start charging ...")
		if (isCharging(regex_charge, result) == True):
			print ("No need to send request we are already charging ...")
			pass
		else:
			req = urllib.request.Request(url=url, data=DATA_ON,method='PUT')
			try:
				with urllib.request.urlopen(req, context=ssl._create_unverified_context()) as f:
				    pass
			except:
				pass

	if (battery_level >= limit_upper):
		print ("Stop charging ...")
		if (isCharging(regex_charge, result) == False):
			print ("No need to send request we are not charging ...")
			pass
		else:
			req = urllib.request.Request(url=url, data=DATA_OFF,method='PUT')
			try:
				with urllib.request.urlopen(req, context=ssl._create_unverified_context()) as f:
				    pass
			except:
				pass

	break
	#time.sleep(time_to_sleep)
	

