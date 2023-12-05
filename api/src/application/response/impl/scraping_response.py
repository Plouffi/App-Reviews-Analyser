from typing import Dict

from src.application.response.a_response import AResponse

class ScrapingResponse(AResponse):

	msg: str

	def __init__(self, msg: str) -> None:
		self.msg = msg

	def to_json(self) -> Dict:
		return {
				'msg': self.msg,
			}