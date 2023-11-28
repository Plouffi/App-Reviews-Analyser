from typing import Dict
from abc import ABC, abstractmethod
from flask import Response

class TypeResponse:
	"""Enum to represente the exporting status of reviews"""
	JSON = 'json'
	PNG = 'png'

class AResponse(ABC):

	@abstractmethod
	def to_json(self) -> Dict:
		pass

	@abstractmethod
	def image_data(self) -> bytes:
		pass

	def response(self, type) -> Response:
		if (type == TypeResponse.JSON):
			return Response(response=self.to_json(), status=200, mimetype='application/json')
		elif (type == TypeResponse.PNG):
			return Response(response=self.image_data(), status=200, mimetype='image/png')
		else:
			raise TypeError(f"Can't handle response type: {type}")
