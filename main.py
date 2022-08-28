import http.client
import time

conn = http.client.HTTPConnection("192.168.0.106")

for i in range(0, 10):
	print(i)
	if i % 2 == 0:
		conn.request("GET", "/YamahaExtendedControl/v1/main/getStatus")
	else:
		conn.request("GET", "/YamahaExtendedControl/v1/main/setVolume?volume=101")

	res = conn.getresponse()
	json = res.read()


