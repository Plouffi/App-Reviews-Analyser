from typing import Dict
from io import BytesIO

from src.application.response.a_response import AResponse

class ImageResponse(AResponse):

	image_data: BytesIO

	def __init__(self, image_data: BytesIO) -> None:
		self.image_data = image_data

	def to_image_data(self) -> bytes:
		return self.image_data.getvalue()
	
	def to_json(self) -> Dict:
		pass