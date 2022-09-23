# FLiP-Py-Jetson-Sensors
Waveshare Environmental Sensor Board on Jetson Nano 2GB - Apache Pulsar - Python 3.10 - Ubuntu 18.04

![Jetson Nano](https://raw.githubusercontent.com/tspannhw/FLiP-Py-Jetson-Sensors/main/jetsonnano.png)


### Upgrade

````
Let's get Python 3.10

apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget -y
apt-get install python3-smbus -y
apt-get install python3-pil -y
apt-get install i2c-tools -y

wget https://www.waveshare.com/w/upload/a/a2/Environment_sensor_fot_jetson_nano.7z

wget https://www.python.org/ftp/python/3.10.6/Python-3.10.6.tgz

tar -xvf Python-3.10.6.tgz
cd Python-3.10.6
./configure --enable-optimizations
make -j $(nproc)  --with-openssl
sudo -H make altinstall
/usr/local/bin/python3.10
/usr/local/bin/pip3.10 install --upgrade pip
/usr/local/bin/pip3.10 install pulsar-client
/usr/local/bin/pip3.10 install pulsar-client[all]
pip3.10 install pillow
cat /etc/os-release
htop
jtop
pip3.10 install -U jetson-stats
````

### Pulsar Consume

````
bin/pulsar-client consume "persistent://public/default/jetsonsensors" -s jtsnr4 -n 0


----- got message -----
key:[nano_uuid_wio_20220826204650], properties:[], content:{
 "uuid": "nano_uuid_wio_20220826204650",
 "ipaddress": "192.168.1.217",
 "cputempf": 81,
 "gputempf": 81,
 "runtime": 6,
 "host": "nano2gb-desktop",
 "hostname": "nano2gb-desktop",
 "macaddress": "1c:bf:ce:1a:7f:a0",
 "endtime": "1661546810.3255336",
 "te": "5.542823791503906",
 "cpu": 12.9,
 "diskusage": "21372.4 MB",
 "memory": 33.8,
 "rowid": "20220826204650_3bed1e8a-9471-4aec-ada0-d04400d882ed",
 "systemtime": "08/26/2022 16:46:50",
 "ts": 1661546810,
 "starttime": "1661546804.7827098",
 "datetimestamp": null,
 "temperature": 23.47,
 "humidity": 56.73,
 "uv": 0.03,
 "ir": 259.0,
 "pressure": 1008.05,
 "jetsontime": "08/26/2022",
 "uptime": "2 days, 1:30:45.580000",
 "tempgpu": "27.0",
 "tempcpu": "28.0"
}
````


### JSON Data

````
{ 'uuid': 'nano_uuid_mvc_20220826165941', 'ipaddress': '192.168.1.217', 'cputempf': 81, 'gputempf': 80, 'runtime': 6, 'host': 'nano2gb-desktop', 'hostname': 'nano2gb-desktop', 'macaddress': '1c:bf:ce:1a:7f:a0', 'endtime': '1661533181.2241657', 'te': '6.468578100204468', 'cpu': 15.5, 'diskusage': '21372.4 MB', 'memory': 33.6, 'rowid': '20220826165941_1b1eff0a-4750-450d-a5e3-184063197e4f', 'systemtime': '08/26/2022 12:59:41', 'ts': 1661533181, 'starttime': '1661533174.7555876', 'datetimestamp': None, 'temperature': 23.45, 'humidity': 56.26, 'uv': 0.03, 'ir': 258.0, 'pressure': 1009.89, 'jetsontime': '08/26/2022', 'uptime': '1 day, 21:43:36.520000', 'tempgpu': '26.5', 'tempcpu': '27.5'}
````

### References

* https://github.com/tspannhw/SettingUpAJetsonNano2GB
* https://www.influxdata.com/blog/nvidia-jetson-series-part-1-jetson-stats/
* https://github.com/rbonghi/jetson_stats
* https://github.com/tspannhw/FutureFLiPNS
* https://github.com/makepluscode/jetson-stats-zeromq
* https://github.com/Jayclifford345/demo_telegraf_jetson_stats
* https://www.waveshare.com/environment-sensor-for-jetson-nano.htm
* https://www.waveshare.com/wiki/Environment_Sensor_for_Jetson_Nano
* https://www.datainmotion.dev/2020/10/flank-streaming-edgeai-on-new-nvidia.html



![Jetson Nano](https://raw.githubusercontent.com/tspannhw/FLiP-Py-Jetson-Sensors/main/IMG-2099.JPG)
