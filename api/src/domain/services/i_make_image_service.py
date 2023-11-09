from typing import Tuple, List
from PIL import Image
from abc import ABC, abstractmethod


class IMakeImageService(ABC):

	@abstractmethod
	def simple_image(words: List[Tuple[str, float]]) -> Image:
		"""Generate wordcloud image.
		----------
		Parameters:
		words (List[Tuple[str, float]]): A list of words and their frequencies
		"""
		pass