from typing import Dict, Tuple, List
import numpy as np
import pandas as pd
from pandas import DataFrame
from datetime import datetime as dt
from datetime import timedelta

from src.domain.repository.reviews_repository import IReviewsRepository

class AnalyserService:
	"""
	A class to handle and compute statistics.
	...
		Attributes
		----------
		config : Dict
			Program's configuration.
		df : Dataframe
	"""
	df: DataFrame
	reviews_df_repo: IReviewsRepository
	
	def __init__(self, config, reviews_df_repo: IReviewsRepository):
		"""
			Parameters
			----------
			config : Dict
				Program's configuration.

		"""
		self.config = config
		self.reviews_df_repo = reviews_df_repo
		self.df = self.reviews_df_repo.load()

	def get_num_reviews(self) -> int:
		"""
		Method to load reviews from csv file. Set up the dataframe's index on "at" column (publication date)
			Returns 
			-------
				int
				The number of reviews
		"""
		dfpy = self.reviews_df_repo.get_series("score").to_numpy()
		return len(dfpy)

	def compute_mean(self) -> Tuple[np.ndarray, int]:
		"""
		Method to compute mean of reviews' score.
			Returns
			-------
				Tuple[np.ndarray,int]
					The mean and the number of reviews
		"""
		dfpy = self.reviews_df_repo.get_series("score").to_numpy()
		return np.mean(dfpy), len(dfpy)

	def compute_rolling_mean(self, time_delta: int, nb_ignore: int = 1000) -> pd.Series:
		"""
		Method to compute rolling mean of reviews' score. Time_delta parameters define the rolling time window in days to compute result,
		nb_ignore parameter remove an arbitrary amount of data in head to avoid irrelevant data while computing first values.
		For more infos about time window, see https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
			Returns
			-------
				pd.Series
		"""
		time_delta = str(time_delta) + 'D'
		return self.reviews_df_repo.get_series("score").iloc[nb_ignore:].rolling(time_delta).mean()

	def compute_cumulative_mean(self, nb_ignore: int = 1000) -> pd.Series:
		"""
		Method to compute cumulative mean of reviews' score.
		nb_ignore parameter remove an arbitrary amount of data in head to avoid irrelevant data while computing first values.
			Returns
			-------
				pd.Series
		"""
		return self.reviews_df_repo.get_series("score").iloc[nb_ignore:].expanding().mean()

	def compute_rolling_sum(self, time_delta: int, nb_ignore: int = 1000) -> pd.Series:
		"""
		Method to compute rolling sum of reviews. Time_delta parameters define the rolling time window in days to compute result,
		nb_ignore parameter remove an arbitrary amount of data in head to avoid irrelevant data while computing first values.
		For more infos about time window, see https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
			Returns
			-------
				pd.Series
		"""
		time_delta = str(time_delta) + 'D'
		return self.reviews_df_repo.get_series("score").iloc[nb_ignore:].rolling(time_delta).count()
	
	def compute_score_distribution(self, date: dt) -> Tuple[List[List[float]], List[int]]:
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

		tomorrow = dt.now() + timedelta(1)
		mask_before = (self.df.index < date) if date is not None else (self.df.index < tomorrow)
		before_fp = self.reviews_df_repo.get_reviews_from_mask(mask_before)
		after_fp = self.reviews_df_repo.get_reviews_from_mask(self.df.index >= date) if date is not None else None

		return [get_score_distribution(before_fp), get_score_distribution(after_fp)], [len(before_fp), len(after_fp) if date is not None else 0]

	def compute_mention(self, lang: str, keywords: List[str]) -> Tuple[pd.Series,  pd.Series, pd.Series]:
		""",
		Method to compute stats about mentions in selected language reviews. Native detection, check if the content one
		of the keywords defined in the configuration file.
			Returns
			-------
			Tuple[pd.Series,  pd.Series, pd.Series]
		"""
		mask_language = self.reviews_df_repo.get_series("language") == lang
		#mask_period = self.df.index >= self.feh_pass_date
		mask_mention = self.reviews_df_repo.get_series("content").str.contains('|'.join(keywords))
		mask_score = self.reviews_df_repo.get_series("score") == 1
		mask = mask_language #& mask_period
		mask_with_mention = mask & mask_mention
		mask_1star_with_mention = mask_with_mention & mask_score

		return (self.reviews_df_repo.get_reviews_from_mask(mask),
			self.reviews_df_repo.get_reviews_from_mask(mask_with_mention),
			self.reviews_df_repo.get_reviews_from_mask(mask_1star_with_mention))