from typing import List, Tuple
import numpy as np
from PIL import Image
from wordcloud import WordCloud
defaultwords = [("No data", 0.70), ("NaN", 0.25), ("nada", 0.025), ("rien", 0.025)]
width = 400
height = 200
scaling = 2


def simple_image(words: List[Tuple[str, float]]) -> Image:
	if len(words) <= 0:
		words = defaultwords
	# we create the mask image
	mask = np.zeros(shape=(height, width), dtype=int)

	# generate the image
	imgobject: Image = WordCloud(
		"Image/Fonts/OpenSansEmoji.otf", scale=scaling, max_words=None, mask=mask,
		background_color=None, mode="RGBA"
	).fit_words(dict(words)).to_image()

	return imgobject
