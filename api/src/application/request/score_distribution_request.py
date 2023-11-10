from datetime import datetime
from flask import Request


class ScoreDistributionRequest():

	app_id: str
	date: datetime

	def __init__(self, request: Request) -> None:
		self.app_id = str(request.get_json()['app_id'])
		self.date = request.get_json().get('date', None)