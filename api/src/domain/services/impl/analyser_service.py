from typing import Dict, Tuple, List, Any
import numpy as np
from pandas import DataFrame, Series
from datetime import datetime as dt
from datetime import timedelta

from src.domain.model.gps_app import GPSApp
from src.domain.repository.gps_app_repository import IGPSAppRepository
from src.domain.repository.reviews_repository import IReviewsRepository
from src.domain.services.i_analyser_service import IAnalyserService

class AnalyserService(IAnalyserService):
	"""Service computing statics on app reviews
		----------
		Attributes:
		config (Dict): Program's configuration
		reviews_repo (IReviewsRepository): Reviews repository
		gps_app_repo (IGPSAppRepository): GPS app repository
	"""
	config: Dict
	reviews_repo: IReviewsRepository
	gps_app_repo: IGPSAppRepository
	
	def __init__(self, config, reviews_repo: IReviewsRepository, gps_app_repo: IGPSAppRepository):
		self.config = config
		self.gps_app_repo = gps_app_repo
		self.reviews_repo = reviews_repo

	def num_reviews(self, app_id: str) -> int:
		app = GPSApp(self.gps_app_repo.get(app_id))
		if app is not None:
			df = self.reviews_repo.get_df(app.exportPath)
			dfpy = self.reviews_repo.get_series(df, "score").to_numpy()
			return len(dfpy)
		else:
			return 0

	def mean(self, app_id:str) -> Tuple[np.ndarray, int]:
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
		Compute rolling mean of reviews' score. Time_delta parameters define the rolling time window in days to compute result,
		nb_ignore parameter remove an arbitrary amount of data in head to avoid irrelevant data while computing first values.
		For more infos about time window, see https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
		----------
		Returns:
		Series: Rolling mean
		"""
		time_delta = str(time_delta) + 'D'
		return self.reviews_repo.get_series(df, "score").iloc[nb_ignore:].rolling(time_delta).mean()

	def cumulative_mean(self, df: DataFrame, nb_ignore: int = 1000) -> Series:
		"""Compute cumulative mean of reviews' score.
		nb_ignore parameter remove an arbitrary amount of data in head to avoid irrelevant data while computing first values.
		----------
		Returns:
		Series: Cumulative mean
		"""
		return self.reviews_repo.get_series(df, "score").iloc[nb_ignore:].expanding().mean()

	def rolling_sum(self, df: DataFrame, time_delta: int, nb_ignore: int = 1000) -> Series:
		"""
		Compute rolling sum of reviews. Time_delta parameters define the rolling time window in days to compute result,
		nb_ignore parameter remove an arbitrary amount of data in head to avoid irrelevant data while computing first values.
		For more infos about time window, see https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
		----------
		Returns:
		Series: Rolling sum
		"""
		time_delta = str(time_delta) + 'D'
		return self.reviews_repo.get_series(df, "score").iloc[nb_ignore:].rolling(time_delta).count()
	
	def score_distribution(self, app_id: str, date: dt) -> Tuple[List[List[float]], List[int]]:
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

	def mentions(self, app_id: str, lang: str, keywords: List[str]) -> Tuple[Series, Series, Series]:
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