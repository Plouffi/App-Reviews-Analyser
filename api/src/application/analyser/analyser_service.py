from typing import Dict, Tuple, List, Any
import numpy as np
from pandas import DataFrame, Series
from datetime import datetime as dt
from datetime import timedelta

from src.domain.model.gps_app import GPSApp
from src.domain.repository.gps_app_repository import IGPSAppRepository
from src.domain.repository.reviews_repository import IReviewsRepository

class AnalyserService:
	"""
	A class to handle and compute statistics.
	...
		Attributes
		----------
		config : Dict
			Program's configuration.
	"""
	gps_app_repo: IGPSAppRepository
	reviews_repo: IReviewsRepository
	
	def __init__(self, config, gps_app_repo: IGPSAppRepository, reviews_repo: IReviewsRepository):
		"""
			Parameters
			----------
			config : Dict
				Program's configuration.

		"""
		self.config = config
		self.gps_app_repo = gps_app_repo
		self.reviews_repo = reviews_repo

	def num_reviews(self, app_id: str) -> int:
		"""
		Method to load reviews from csv file. Set up the dataframe's index on "at" column (publication date)
			Returns 
			-------
				int
				The number of reviews
		"""
		app = GPSApp(self.gps_app_repo.get(app_id))
		if app is not None:
			df = self.reviews_repo.get_df(app.exportPath)
			dfpy = self.reviews_repo.get_series(df, "score").to_numpy()
			return len(dfpy)
		else:
			return 0

	def mean(self, app_id:str) -> Tuple[np.ndarray, int]:
		"""
		Method to compute mean of reviews' score.
			Returns
			-------
				Tuple[np.ndarray,int]
					The mean and the number of reviews
		"""
		app = GPSApp(self.gps_app_repo.get(app_id))
		if app is not None:
			df = self.reviews_repo.get_df(app.exportPath)
			dfpy = self.reviews_repo.get_series(df, "score").to_numpy()
			return np.mean(dfpy), len(dfpy)
		else:
			return None, 0

	def means_stats(self, app_id: str, time_delta: int, nb_ignore: int = 1000) -> Tuple[Series,  Series, Series]:
		app = GPSApp(self.gps_app_repo.get(app_id))
		if app is not None:
			df = self.reviews_repo.get_df(app.exportPath)
			mean = self.cumulative_mean(df, time_delta, nb_ignore)
			rolling_mean = self.rolling_mean(df, time_delta, nb_ignore)
			rolling_sum = self.rolling_sum(df, time_delta, nb_ignore)
			return mean, rolling_mean, rolling_sum


	def rolling_mean(self, df: DataFrame, time_delta: int, nb_ignore: int = 1000) -> Series:
		"""
		Method to compute rolling mean of reviews' score. Time_delta parameters define the rolling time window in days to compute result,
		nb_ignore parameter remove an arbitrary amount of data in head to avoid irrelevant data while computing first values.
		For more infos about time window, see https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
			Returns
			-------
				Series
		"""
		time_delta = str(time_delta) + 'D'
		return self.reviews_repo.get_series(df, "score").iloc[nb_ignore:].rolling(time_delta).mean()

	def cumulative_mean(self, df: DataFrame, nb_ignore: int = 1000) -> Series:
		"""
		Method to compute cumulative mean of reviews' score.
		nb_ignore parameter remove an arbitrary amount of data in head to avoid irrelevant data while computing first values.
			Returns
			-------
				Series
		"""
		return self.reviews_repo.get_series(df, "score").iloc[nb_ignore:].expanding().mean()

	def rolling_sum(self, df: DataFrame, time_delta: int, nb_ignore: int = 1000) -> Series:
		"""
		Method to compute rolling sum of reviews. Time_delta parameters define the rolling time window in days to compute result,
		nb_ignore parameter remove an arbitrary amount of data in head to avoid irrelevant data while computing first values.
		For more infos about time window, see https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
			Returns
			-------
				Series
		"""
		time_delta = str(time_delta) + 'D'
		return self.reviews_repo.get_series(df, "score").iloc[nb_ignore:].rolling(time_delta).count()
	
	def score_distribution(self, app_id: str, date: dt) -> Tuple[List[List[float]], List[int]]:
		"""
		Method to compute score distribution before and after the date parameter. If date is None, it is considered as tomorrow
			Returns
			-------
			List(List(int))
				A 2-dimensionnal array representing score distribution before and after FEH pass.
				Shape should be (2, 5) 2--> before/after // 5--> score range
			List(int)
				An array stocking the number of reviews published before and after FEH pass
		"""
		def get_score_distribution(data):
			if data is None:
				return None
			score_distribution = []
			for i in range(5, 0, -1):
				pourcent = len(data.loc[data["score"] == i]) / len(data) * 100
				score_distribution.append(pourcent)
			return score_distribution
		
		app = GPSApp(self.gps_app_repo.get(app_id))
		if app is not None:
			df = self.reviews_repo.get_df(app.exportPath)
			tomorrow = dt.now() + timedelta(1)
			mask_before = (self.reviews_repo.get_index(df) < date) if date is not None else (self.reviews_repo.get_index(df) < tomorrow)
			before_fp = self.reviews_repo.get(mask_before)
			after_fp = self.reviews_repo.get(self.reviews_repo.get_index(df) >= date) if date is not None else None
			return [get_score_distribution(before_fp), get_score_distribution(after_fp)], [len(before_fp), len(after_fp) if date is not None else 0]
		else:
			return None, None

	def mentions(self, app_id: str, lang: str, keywords: List[str]) -> Tuple[Series,  Series, Series]:
		""",
		Method to compute stats about mentions in selected language reviews. Native detection, check if the content one
		of the keywords defined in the configuration file.
			Returns
			-------
			Tuple[Series,  Series, Series]
		"""
		app = GPSApp(self.gps_app_repo.get(app_id))
		if app is not None:
			df = self.reviews_repo.get_df(app.exportPath)
			mask_language = self.reviews_repo.get_series(df, "language") == lang
			#mask_period = self.df.index >= self.feh_pass_date
			mask_mention = self.reviews_repo.get_series(df, "content").str.contains('|'.join(keywords))
			mask_score = self.reviews_repo.get_series(df, "score") == 1
			mask = mask_language #& mask_period
			mask_with_mention = mask & mask_mention
			mask_1star_with_mention = mask_with_mention & mask_score

		return (self.reviews_repo.get(mask),
			self.reviews_repo.get(mask_with_mention),
			self.reviews_repo.get(mask_1star_with_mention))