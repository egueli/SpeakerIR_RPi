import http.client
import json

class MusicCast:
	def __init__(self):
		self._conn = http.client.HTTPConnection("192.168.0.106")

	def get_volume(self):
		yxc_status = self._do_yxc_request(f"getStatus")
		return yxc_status['volume']

	def set_volume(self, volume):
		self._do_yxc_request(f"setVolume?volume={volume}")

	def _do_yxc_request(self, query):
		self._conn.request("GET", f"/YamahaExtendedControl/v1/main/{query}")
		res = self._conn.getresponse()
		res_body = res.read()
		yxc_status = json.loads(res_body)
		response_code = yxc_status['response_code']
		if response_code != 0:
			raise YXCNonZeroResponseCodeException(response_code)
		return yxc_status


class YXCNonZeroResponseCodeException(Exception):
    def __init__(self, code):
        self.code = code