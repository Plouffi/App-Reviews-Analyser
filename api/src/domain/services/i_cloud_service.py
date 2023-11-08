from typing import List, Tuple
from abc import ABC, abstractmethod

from src.domain.model.review import Review


class ICloudService(ABC):

	@abstractmethod
	def load_reviews(self, alpha: int = 1, n: int = 2, *data_reviews: List[Review]):
		"""Method to fill vocabulary and occurences and counts.
		----------
			Parameters:
			alpha (int): Noise reducer
			n (int): Number of words per token vocabulary
			*data_reviews (Tuple[List[Review]]): List of reviews
		"""
		pass

	@abstractmethod
	def word_cloud(self, index: int, words: int = 50) -> List[Tuple[str, float]]:
		"""Method to return the top 50 words of each set of reviews.
			----------
			Parameters:
			index (int): Index of the set of review
			words (int): Number of top words selected (default=50)
			----------
			Returns:
			List[Tuple[str, float]]: The list of top words and their frequencies
		"""
		pass
	
	@abstractmethod
	def get_words(self) -> List[List[Tuple[str, float]]]:
		"""Save the reviews correponding to the app ID into a cvs file
		----------
		Parameters:
		app_id (str): the app ID
		----------
		Returns:
		None
		"""
		pass
		