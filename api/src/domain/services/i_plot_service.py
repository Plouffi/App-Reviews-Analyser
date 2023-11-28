from typing import Dict, List
from abc import ABC, abstractmethod
from datetime import datetime as dt
from pandas import Series
from matplotlib.figure import Figure


class IPlotService(ABC):
  
	@abstractmethod
	def means(self, cumulative_mean: Series, rolling_mean: Series, rolling_sum: Series) -> Figure:
		"""Return a Figure of a graph displaying curves of rolling average and cumulative mean.
				----------
		Parameters:
		stats (Dict):	A dictionnaire of data containing the cumulative mean, the rolling mean and the rolling sum data
		----------
		Returns:
		Figure: A plot figure
		"""
		pass

	@abstractmethod
	def score_distribution(self, reviews_distribution: List[List[float]], nb_reviews: List[int], date: dt) -> Figure:
		"""Return a figure of a bar chart showing reviews' score ditribution between 2 periods of time. If date is None,
		return only 1 bar chart (no comparaison)
		----------
		Parameters:
		reviews_distribution (List(List(float))):	A 2-dimensionnal array representing score distribution before and after date.
			Shape should be (2, 5) 2--> before/after // 5--> score range
		nb_reviews (List(int)):	An array stocking the number of reviews published before and after date
		----------
		Returns:
		Figure: A plot figure
		"""
		pass

	@abstractmethod
	def refresh(self) -> None:
		"""Refresh the current plot"""
		pass