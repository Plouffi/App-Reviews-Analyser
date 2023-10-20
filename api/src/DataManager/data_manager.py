from typing import Dict, Tuple, List
import numpy as np
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta

class DataManager:
	"""
	A class to handle and compute statistics.
	...
		Attributes
		----------
		config : Dict
			Program's configuration.
		df : Dataframe
	"""
	def __init__(self, config):
		"""
			Parameters
			----------
			config : Dict
				Program's configuration.

		"""
		columns = ["userName", "content", "score", "thumbsUpCount", "reviewCreatedVersion", "at", "language"]
		self.df = pd.DataFrame(columns=columns)
		self.config = config

	def insert_reviews(self, reviews):
		"""
		Method to store data review in a Dataframe
			Parameters
			----------
			reviews : Lis(Dict)
				Array of dictionnary containing data review

		"""
		series_reviews = []
		for review in reviews:
			series_reviews.append(pd.Series(review.items(), index=self.df.columns))
		self.df = self.df._append(reviews, ignore_index=True)

	def get_reviews(self):
		"""
		Return the Dataframe
		"""
		return self.df

	def get_reviews_as_dict(self, start_date: dt, end_date: dt, language: str = "en", score: int = -1) -> Dict:
		"""
		Method to research reviews by passing parameters (language, date, period, score). Return them as a dictionnary
			Parameters
			----------
			start_date : datetime
				Research parameter: date where we start the research.
			end_date : datetime
				Research parameter: date where we end the research.
			language : str = "en"
				Research parameter: review's language. Set up to "en" if language doesn't exist in configuration file.
				/ "after" same logic
			score : int = -1
				Research parameter: review's score. Can be in [1...5] or anything else to have all range
			Returns
			-------
				Dict
					A dictionnary of reviews
		"""
		mask_language = self.df["language"] == language if language in self.config["languages"] else "en"
		mask_start_period = start_date <= self.df.index
		mask_end_period = self.df.index < end_date
		mask_score = self.df["score"] == score if 0 < score <= 5 else self.df["score"].isin([1, 2, 3, 4, 5])
		mask = mask_language & mask_start_period & mask_end_period & mask_score

		return self.df.loc[mask].to_dict('records')

	def load(self):
		"""
		Method to load reviews from csv file. Set up the dataframe's index on "at" column (publication date)
		"""
		self.df = pd.read_csv(self.config["export_path"])
		# set up the index on publishing date and sort the dataframe
		self.df["at"] = pd.to_datetime(self.df["at"])
		self.df = self.df.set_index("at")
		self.df = self.df.sort_values("at", ascending=True)

	def export(self):
		"""
		Method to export reviews in csv.
		"""
		self.df.to_csv(self.config["export_path"], index=False)
		print(f"Reviews exported in '{self.config['export_path']}'. Total: {len(self.df.index)} records.")

	def get_num_reviews(self) -> int:
		"""
		Method to load reviews from csv file. Set up the dataframe's index on "at" column (publication date)
			Returns
			-------
				int
				The number of reviews
		"""
		dfpy = self.df["score"].to_numpy()
		return len(dfpy)

	def compute_mean(self) -> Tuple[np.ndarray, int]:
		"""
		Method to compute mean of reviews' score.
			Returns
			-------
				Tuple[np.ndarray,int]
					The mean and the number of reviews
		"""
		dfpy = self.df["score"].to_numpy()
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
		return self.df["score"].iloc[nb_ignore:].rolling(time_delta).mean()

	def compute_cumulative_mean(self, nb_ignore: int = 1000) -> pd.Series:
		"""
		Method to compute cumulative mean of reviews' score.
		nb_ignore parameter remove an arbitrary amount of data in head to avoid irrelevant data while computing first values.
			Returns
			-------
				pd.Series
		"""
		return self.df["score"].iloc[nb_ignore:].expanding().mean()

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
		return self.df["score"].iloc[nb_ignore:].rolling(time_delta).count()
	
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
		before_fp = self.df.loc[(self.df.index < date)] if date is not None else self.df.loc[(self.df.index < tomorrow)]
		after_fp = self.df.loc[(self.df.index >= date)] if date is not None else None

		return [get_score_distribution(before_fp), get_score_distribution(after_fp)], [len(before_fp), len(after_fp) if date is not None else 0]

	def compute_mention(self, lang: str, keywords: List[str]) -> Tuple[pd.Series,  pd.Series, pd.Series]:
		""",
		Method to compute stats about mentions in selected language reviews. Native detection, check if the content one
		of the keywords defined in the configuration file.
			Returns
			-------
			Tuple[pd.Series,  pd.Series, pd.Series]
		"""
		mask_language = self.df["language"] == lang
		#mask_period = self.df.index >= self.feh_pass_date
		mask_mention = self.df["content"].str.contains('|'.join(keywords))
		mask_score = self.df["score"] == 1
		mask = mask_language #& mask_period
		mask_with_mention = mask & mask_mention
		mask_1star_with_mention = mask_with_mention & mask_score

		return self.df.loc[mask], self.df.loc[mask_with_mention], self.df.loc[mask_1star_with_mention]