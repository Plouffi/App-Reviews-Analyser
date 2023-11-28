from typing import List, Tuple, Dict
import numpy as np
from PIL import Image
from wordcloud import WordCloud
from dependency_injector.providers import Configuration

from src.domain.services.i_make_image_service import IMakeImageService

class MakeImageService(IMakeImageService):
	"""A class to generate wordcloud image.
		----------
		Attributes
		path_to_font (str): Path to the font file
		defaultwords (List[Tuple[str, float]]): Default words if no is provided
	"""
	path_to_font: str
	defaultwords: List[Tuple[str, float]]

	def __init__(self, config: Dict):
		self.path_to_font = config['wordcloudFont']
		self.defaultwords = [("No data", 0.70), ("NaN", 0.25), ("nada", 0.025), ("rien", 0.025)]

	def simple_image(self, words: List[Tuple[str, float]]) -> Image:
		width = 400
		height = 200
		scaling = 2
		if len(words) <= 0:
			words = self.defaultwords
		# we create the mask image
		mask = np.zeros(shape=(height, width), dtype=int)

		# generate the image
		imgobject: Image = WordCloud(
			self.path_to_font, scale=scaling, max_words=None, mask=mask,
			background_color=None, mode="RGBA"
		).fit_words(dict(words)).to_image()

		return imgobject
