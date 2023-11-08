from typing import List
from abc import ABC, abstractmethod
from datetime import datetime as dt
from src.domain.model.gps_app import GPSApp
from src.domain.model.review import Review


class IGPSService(ABC):

	@abstractmethod
	def get_app(self, app_id: str) -> GPSApp:
		"""Returns a GPS app.
		----------
		Parameters:
		app_id (str): the app ID
		----------
		Returns:
		GPSApp: The GPS app
		"""
		pass

	@abstractmethod
	def get_reviews(self, app_id: str, start_date: dt, end_date: dt, language: str = "en", score: int = -1) -> List[Review]:
		"""Returns a set of reviews based on various parameter of the selected app ID.
		----------
		Parameters:
		app_id (str): the app ID
		start_date (datetime): Start date request parameter, define the upper date of research
		end_date (datetime): End date request parameter, define the lower date of research
		language (str): Language request parameter, defines the language reviews. (default = "en")
		score (int): Score request parameter, defines the score reviews between 1 and 5, if score < 0, it
		selects all score reviews (default = -1)
		----------
		Returns:
		List[Reviews]: The filtered reviews, empty if the app was not found
		"""
		pass

	@abstractmethod
	def save_app(self, app_id: str) -> None:
		"""Save the app correponding to the app ID into the database
		----------
		Parameters:
		app_id (str): the app ID
		----------
		Returns:
		None
		"""
		pass

	@abstractmethod
	def save_reviews(self, app_id: str) -> None:
		"""Save the reviews correponding to the app ID into a cvs file
		----------
		Parameters:
		app_id (str): the app ID
		----------
		Returns:
		None
		"""
		pass