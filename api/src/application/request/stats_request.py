from flask import Request


class StatsRequest():

	app_id: str
	lang: str
	keywords: str

	def __init__(self, request: Request) -> None:
		self.app_id = str(request.get_json()['appId'])
		self.lang = str(request.get_json()['lang'])
		self.keywords = request.get_json()['keywords']