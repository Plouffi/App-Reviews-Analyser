from typing import Any
from io import BytesIO

from src.application.response.a_response import AResponse

class ImageResponse(AResponse):

	image_data: BytesIO

	def __init__(self, image_data: BytesIO) -> None:
		self.image_data = image_data

	def image_data(self) -> bytes:
		return self.image_data.getvalue()