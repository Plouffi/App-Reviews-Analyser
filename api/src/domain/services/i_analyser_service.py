from typing import Tuple, List
import numpy as np
from pandas import Series
from datetime import datetime as dt
from abc import ABC, abstractmethod


class IAnaliserService(ABC):
  
	@abstractmethod
	def num_reviews(self, app_id: str) -> int:
		"""Count the number of reviews of the selected app
			----------
			Parameters:
			app_id (str): The app ID
			----------
			Returns 
			-------
			int: The number of reviews
		"""
		pass

	@abstractmethod
	def mean(self, app_id: str) -> Tuple[np.ndarray, int]:
		"""Compute the mean of reviews score fo the selected app.
			----------
			Parameters:
			app_id (str): The app ID
			----------
			Returns:
			Tuple[np.ndarray, int]: The mean and the number of reviews
		"""
		pass

	@abstractmethod
	def means_stats(self, app_id: str, time_delta: int, nb_ignore: int = 0) -> Tuple[Series, Series, Series]:
		"""Compute means (cumulative mean, rolling mean and rolling sum) of reviews score fo the selected app.
			----------
			Parameters:
			app_id (str): The app ID
			time_delta (int): Time window in days for the rolling mean and sum
			nb_ignore (int): Number of ignored first reviews (default=0)
			----------
			Returns:
			Tuple[Series, Series, Series]: The mean and the number of reviews
		"""
		pass
	
	@abstractmethod
	def score_distribution(self, app_id: str, date: dt) -> Tuple[List[List[float]], List[int]]:
		"""Compute score distribution before and after the date parameter. If date is None, it is considered as tomorrow
		----------
		Parameters:
		app_id (str): The app ID
		date (datetime): Date to divide the score distbution
		----------
		Returns:
		Tuple[List, List]:
			List(List(int)): A 2-dimensionnal array representing score distribution before and after a date.
			Shape should be (2, 5) 2--> before/after // 5--> score range
			List(int): An array stocking the number of reviews published before and after FEH pass
		"""
		pass

	@abstractmethod
	def mentions(self, app_id: str, lang: str, keywords: List[str]) -> Tuple[Series, Series, Series]:
		"""Method to compute stats about mentions in selected language reviews. Native detection, check if the content one
		of the keywords defined in the configuration file.
		----------
		Parameters:
		app_id (str): The app ID
		lang (str): The review language 
		keywords (List(str)): The list of words to search and count
		----------
		Returns:
		Tuple[Series, Series, Series]:
			- Series of reviews
			-	Series of reviews with mention
			- Series of reviews scored 1 with mention
		"""
		pass