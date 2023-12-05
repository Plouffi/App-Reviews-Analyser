from flask import Request


class MeansRequest():
	
	app_id: str
	time_delta: int
	nb_ignore: int

	def __init__(self, request: Request) -> None:
		self.app_id = str(request.get_json()['appId'])
		self.time_delta = int(request.get_json().get('timeDelta', 30))
		self.nb_ignore = int(request.get_json().get('ignore', 0))