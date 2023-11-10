from typing import Dict
import numpy as np
from pandas import Series

from src.application.response.a_response import AResponse

class StatsResponse(AResponse):

	means: np.ndarray
	nb_reviews: int
	review_with_mention: Series
	review_in_lang: Series
	review_with_mention_1star: Series

	def __init__(self, means: np.ndarray, nb_reviews: int, review_with_mention: Series, review_in_lang: Series, review_with_mention_1star: Series) -> None:
		self.means = means
		self.nb_reviews = nb_reviews
		self.review_with_mention = review_with_mention
		self.review_in_lang = review_in_lang
		self.review_with_mention_1star = review_with_mention_1star

	def to_json(self) -> Dict:
		return {
				'means': self.means,
				'nb_reviews': self.nb_reviews,
				'review_in_lang': len(self.review_in_lang),
				'review_with_mention': len(self.review_with_mention),
				'review_with_mention_1star': len(self.review_with_mention_1star)
			}