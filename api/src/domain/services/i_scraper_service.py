from typing import Dict, List
from abc import ABC, abstractmethod
from datetime import datetime as dt

from src.domain.model.gps_app import GPSApp
from src.domain.model.review import Review

class IScraperService(ABC):

	@abstractmethod
	def search_app(self, search: str) -> List[GPSApp]:
		"""Search apps on the Google Playstore based on search terms
		----------
		Parameters:
		search (str): Search terms
		----------
		Returns:
		List[GPSApp]: List of detail app from the search result
		"""
		pass

	@abstractmethod
	def app_detail(self, app_id: str) -> GPSApp:
		"""Retrieve all informations about an app on the Google Playstore
		----------
		Parameters:
		app_id (str): The app ID
		----------
		Returns:
		GPSApp: The app
		"""
		pass

	@abstractmethod
	def get_reviews(self, app_id: str, date: dt) -> List[Review]:
		"""Retrieve all reviews from an App on the Google Playstore until a certain date
		----------
		Parameters:
		app_id (str): The app ID
		date (datetime): The date until we stop fetching reviews
		----------
		Returns:
		List[Review]: A list of reviews
		"""
		pass