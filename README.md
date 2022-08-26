# FLiP-Py-Jetson-Sensors
Waveshare Environmental Sensor Board on Jetson Nano 2GB - Apache Pulsar - Python 3.10 - Ubuntu 18.04


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
