import http.client
import json

class MusicCast:
	def is_on(self):
		yxc_status = self._do_yxc_zone_request(f"getStatus")
		return yxc_status['power'] == "on"

	def get_volume(self):
		yxc_status = self._do_yxc_zone_request(f"getStatus")
		return yxc_status['volume']

	def set_volume(self, volume):
		self._do_yxc_zone_request(f"setVolume?volume={volume}")

	def get_is_muted(self):
		yxc_status = self._do_yxc_zone_request(f"getStatus")
		return yxc_status['mute']

	def set_muted(self, muted):
		enable = "true" if muted else "false"
		self._do_yxc_zone_request(f"setMute?enable={enable}")

	def power_on(self):
		self._do_yxc_zone_request(f"setPower?power=on")

	def set_input(self, input):
		self._do_yxc_zone_request(f"setInput?input={input}")

	def set_speaker(self, speaker_name, enable):
		query = "setSpeakerA" if speaker_name == "a" else "setSpeakerB" 
		enable = "true" if enable else "false"
		self._do_yxc_system_request(f"{query}?enable={enable}")

	def _do_yxc_zone_request(self, query):
		return self._do_yxc_request(f"/YamahaExtendedControl/v1/main/{query}")

	def _do_yxc_system_request(self, query):
		return self._do_yxc_request(f"/YamahaExtendedControl/v1/system/{query}")

	def _do_yxc_request(self, path):
		conn = http.client.HTTPConnection("192.168.0.106", timeout=2)
		try:
			n_repeats = 3
			while True:
				try:						
					conn.request("GET", path)
					res = conn.getresponse()
					res_body = res.read()
					yxc_status = json.loads(res_body)
					response_code = yxc_status['response_code']
					if response_code != 0:
						raise YXCNonZeroResponseCodeException(response_code)
					return yxc_status
				except http.client.RemoteDisconnected as e:
					print(f"got RemoteDisconnected, retrying ({n_repeats})")
					n_repeats = n_repeats - 1
					if not n_repeats:
						raise e
		finally:
			conn.close()

class YXCNonZeroResponseCodeException(Exception):
    def __init__(self, code):
        self.code = code