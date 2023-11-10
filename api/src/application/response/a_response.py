from typing import Dict
from abc import ABC, abstractmethod
from flask import Response

class AResponse(ABC):

	@abstractmethod
	def to_json(self) -> Dict:
		pass

	def response(self) -> Response:
		return Response(response=self.to_json(), status=200, mimetype='application/json')