from typing import Dict
import pandas as pd
from datetime import datetime as dt

from src.infrastructure.dataframe.df_repository import DFRepository
from src.domain.repository.reviews_df_repository import IReviewsDFRepository

class ReviewsDF(DFRepository, IReviewsRepository):

	def indexing(self):
		"""
		Method to set up the index on records
		"""
		pass
		super().df["at"] = pd.to_datetime(super().df["at"])
		super().df = super().df.set_index("at")
		super().df = super().df.sort_values("at", ascending=True)
		
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
			series_reviews.append(pd.Series(review.items(), index=super().df.columns))
		super().df = super().df._append(reviews, ignore_index=True)
		self.export()

	def get_reviews(self, start_date: dt, end_date: dt, language: str = "en", score: int = -1) -> Dict:
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
		mask_language = super().df["language"] == language if language in self.config["languages"] else "en"
		mask_start_period = start_date <= super().df.index
		mask_end_period = super().df.index < end_date
		mask_score = super().df["score"] == score if 0 < score <= 5 else super().df["score"].isin([1, 2, 3, 4, 5])
		mask = mask_language & mask_start_period & mask_end_period & mask_score

		return super().df.loc[mask].to_dict('records')