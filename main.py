import http.client

conn = http.client.HTTPConnection("192.168.0.106")

for i in range(0, 10):
	print(i)
	conn.request("GET", "/YamahaExtendedControl/v1/main/getStatus")
	res = conn.getresponse()
	print(res.read())

	conn.request("GET", "/YamahaExtendedControl/v1/main/setVolume?volume=101")
	res = conn.getresponse()
	print(res.read())


