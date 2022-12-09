import http.client
import json

class MusicCast:
	def __init__(self):
		self._conn = None

	def is_on(self):
		yxc_status = self._do_yxc_zone_request(f"getStatus")
		return yxc_status['power'] == "on"

	def get_volume(self):
		yxc_status = self._do_yxc_zone_request(f"getStatus")
		return _vol_n_to_db(yxc_status['volume'])

	def set_volume(self, volume_in_db):
		volume = _vol_db_to_n(volume_in_db)
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
		n_repeats = 3
		while True:
			try:						
				self._get_conn().request("GET", path)
				res = self._get_conn().getresponse()
				res_body = res.read()
				yxc_status = json.loads(res_body)
				response_code = yxc_status['response_code']
				if response_code != 0:
					raise YXCNonZeroResponseCodeException(response_code)
				return yxc_status
			except http.client.HTTPException as e:
				print(f"got {e}, retrying ({n_repeats})")
				self._forget_conn()
				n_repeats = n_repeats - 1
				if not n_repeats:
					raise e
	
	def _get_conn(self):
		if self._conn is None:
			self._conn = http.client.HTTPConnection("Living-Room.local", timeout=1)
		
		return self._conn

	def _forget_conn(self):
		self._conn = None

class YXCNonZeroResponseCodeException(Exception):
    def __init__(self, code):
        self.code = code

def _vol_n_to_db(n):
	return (float(n) - 161) / 2

def _vol_db_to_n(db):
	return int((db * 2) + 161)
