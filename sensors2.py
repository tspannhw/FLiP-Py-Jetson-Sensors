#!/usr/local/bin/python3.10
# -*- coding:utf-8 -*-
import time
import ICM20948 #Gyroscope/Acceleration/Magnetometer
import BME280   #Atmospheric Pressure/Temperature and humidity
import SI1145   #UV
import subprocess
import traceback
import math
import base64
import json
import time
from time import gmtime, strftime
import random, string
import psutil
import uuid
# Importing socket library
import socket
import pulsar
from pulsar.schema import *
from pulsar.schema import AvroSchema
from pulsar.schema import JsonSchema
from pulsar import Client, AuthenticationOauth2
from jtop import jtop
import json, datetime
import argparse
import os.path
import re
import sys
import os
from jtop import jtop

### Schema Object
# https://pulsar.apache.org/docs/en/client-libraries-python/

class jetsonssensor(Record):
    uuid = String(required=True)
    ipaddress = String(required=True)
    cputempf = Integer(required=True)
    gputempf = Integer(required=True)
    runtime = Integer(required=True)
    host = String(required=True)
    hostname = String(required=True)
    macaddress = String(required=True)
    endtime = String(required=True)
    te = String(required=True)
    cpu = Float(required=True)
    diskusage = String(required=True)
    memory = Float(required=True)
    rowid = String(required=True)
    systemtime = String(required=True)
    ts = Integer(required=True)
    starttime = String(required=True)
    datetimestamp = String(required=True)
    temperature = Float(required=True)
    humidity = Float(required=True)
    uv =  Float(required=True)
    ir =  Float(required=True)
    pressure = Float(required=True)
    jetsontime = String(required=True)
    uptime = String(required=True)
    tempgpu = String(required=True)
    tempcpu = String(required=True)

# https://github.com/NVIDIA-AI-IOT/jetbot/issues/18

external_IP_and_port = ('198.41.0.4', 53)  # a.root-servers.net
socket_family = socket.AF_INET

def IP_address():
		try:
			s = socket.socket(socket_family, socket.SOCK_DGRAM)
			s.connect(external_IP_and_port)
			answer = s.getsockname()
			s.close()
			return answer[0] if answer else None
		except socket.error:
			return None

# Get MAC address of a local interfaces
def psutil_iface(iface):
	# type: (str) -> Optional[str]
	import psutil
	nics = psutil.net_if_addrs()
	if iface in nics:
		nic = nics[iface]
		for i in nic:
			if i.family == psutil.AF_LINK:
				return i.address
# Random Word
def randomword(length):
 return ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower()) for i in range(length))

# Timer
start = time.time()
packet_size=3000


# Random Word
def randomword(length):
 return ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower()) for i in range(length))

# Get the temperature of the CPU for compensation
def get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE, universal_newlines=True)
    output, _error = process.communicate()
    return float(output[output.index('=') + 1:output.rindex("'")])

#parse arguments
parse = argparse.ArgumentParser(prog='sensors2.py')
parse.add_argument('-su', '--service-url', dest='service_url', type=str, required=True,
                   help='The pulsar service you want to connect to')
parse.add_argument('-t', '--topic', dest='topic', type=str, required=True,
                   help='The topic you want to produce to')
parse.add_argument('--auth-params', dest='auth_params', type=str, default="",
                   help='The auth params which you need to configure the client')
args = parse.parse_args()

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)

# CPU Temp
f = open("/sys/devices/virtual/thermal/thermal_zone1/temp","r")
cputemp = str( f.readline() )
cputemp = cputemp.replace('\n','')
cputemp = cputemp.strip()
cputemp = str(round(float(cputemp)) / 1000)
cputempf = str(round(9.0/5.0 * float(cputemp) + 32))
f.close()
# GPU Temp
f = open("/sys/devices/virtual/thermal/thermal_zone2/temp","r")
gputemp = str( f.readline() )
gputemp = gputemp.replace('\n','')
gputemp = gputemp.strip()
gputemp = str(round(float(gputemp)) / 1000)
gputempf = str(round(9.0/5.0 * float(gputemp) + 32))
f.close()

ipaddress = IP_address()
threshold = 0.5

bme280 = BME280.BME280()
bme280.get_calib_param()
si1145 = SI1145.SI1145()
icm20948 = ICM20948.ICM20948()

# connect to pulsar
if (len(args.auth_params) == 0 ):
   client = pulsar.Client(args.service_url)
else:
   client = pulsar.Client(args.service_url, authentication=AuthenticationOauth2(args.auth_params))

producer = client.create_producer(topic=args.topic ,schema=JsonSchema(jetsonssensor),properties={"producer-name": "jetson-py-sensor","producer-id": "jetson-sensor" })

try:
	x = 0

	while True:
		#   time.sleep(1)
		if(x < 20):
			bme = []
			bme = bme280.readData() 
			pressure = round(bme[0], 2)
			temp = round(bme[1], 2)
			hum = round(bme[2], 2)
			uv = round(si1145.readdata()[0], 2)
			ir = round(si1145.readdata()[1], 2)
			end = time.time()
			jetsonRec = jetsonssensor()
			# Create unique id
			uniqueid = 'nano_uuid_{0}_{1}'.format(randomword(3),strftime("%Y%m%d%H%M%S",gmtime()))
			uuid2 = '{0}_{1}'.format(strftime("%Y%m%d%H%M%S",gmtime()),uuid.uuid4())

			with jtop() as jetson:
				tmp = jetson.stats
				jetsonRec.jetsontime = str(tmp["time"].strftime('%m/%d/%Y')) 
				jetsonRec.uptime =  str(tmp["uptime"]) 
				jetsonRec.tempgpu = str(tmp["Temp GPU"]) 
				jetsonRec.tempcpu = str(tmp["Temp CPU"]) 

			jetsonRec.pressure = float(pressure)
			jetsonRec.temperature = float(temp)
			jetsonRec.humidity = float(hum)
			jetsonRec.uv = float(uv)
			jetsonRec.ir = float(ir)
			jetsonRec.uuid =  uniqueid
			jetsonRec.ipaddress = ipaddress
			jetsonRec.gputempf =  int(gputempf)
			jetsonRec.cputempf =  int(cputempf)
			jetsonRec.runtime = int(round(end - start))
			jetsonRec.host = os.uname()[1]
			jetsonRec.hostname = host_name
			jetsonRec.macaddress = psutil_iface('wlan0')
			jetsonRec.endtime = '{0}'.format( str(end ))
			jetsonRec.te = '{0}'.format(str(end-start))
			jetsonRec.systemtime = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
			jetsonRec.ts =  int( time.time() )
			jetsonRec.starttime = str(start)
			jetsonRec.cpu = psutil.cpu_percent(interval=1)
			usage = psutil.disk_usage("/")
			jetsonRec.diskusage = "{:.1f} MB".format(float(usage.free) / 1024 / 1024)
			jetsonRec.memory = psutil.virtual_memory().percent
			jetsonRec.rowid = str(uuid2)
			print(jetsonRec)
			producer.send(jetsonRec,partition_key=uniqueid)

except KeyboardInterrupt:
	exit()