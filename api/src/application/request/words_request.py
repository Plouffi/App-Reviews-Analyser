from datetime import datetime
from flask import Request


class WordsRequest():

	app_id: str
	alpha: float
	n: int
	start_date_1: datetime
	start_date_2: datetime
	end_date_1: datetime
	end_date_2: datetime
	lang: str
	score: int

	def __init__(self, request: Request) -> None:
		self.app_id = str(request.get_json()['app_id'])
		self.alpha = float(request.get_json().get('alpha', 10))
		self.n = int(request.get_json().get('n', 2))
		self.start_date_1 = request.get_json()['start1']
		self.start_date_2 = request.get_json()['start2']
		self.end_date_1 = request.get_json()['end1']
		self.end_date_2 = request.get_json()['end2']
		self.lang = str(request.get_json()['lang'])
		self.score = int(request.get_json().get('score', 0))