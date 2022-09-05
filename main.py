import http.client
import time

conn = http.client.HTTPConnection("192.168.0.106")

total_duration = 0
num_samples = 50

for i in range(0, num_samples):
	print(i)
	start_at = time.time()
	if i % 2 == 0:
		conn.request("GET", "/YamahaExtendedControl/v1/main/getStatus")
	else:
		conn.request("GET", "/YamahaExtendedControl/v1/main/setVolume?volume=101")

	res = conn.getresponse()
	json = res.read()
	
	end_at = time.time()
	duration = end_at - start_at
	total_duration = total_duration + duration

	print(f"duration: {duration*1000}ms")

print(f"average: {total_duration*1000/num_samples}ms")


