from typing import Dict
import pandas as pd
import numpy as np
from pandas import Index, Series
from datetime import datetime as dt

from src.infrastructure.dataframe.df_repository import DFRepository
from src.domain.repository.reviews_repository import IReviewsRepository

class ReviewsDF(DFRepository, IReviewsRepository):

	def indexing(self):
		pass
		super().df["at"] = pd.to_datetime(super().df["at"])
		super().df = super().df.set_index("at")
		super().df = super().df.sort_values("at", ascending=True)
		
	def insert_reviews(self, reviews):
		series_reviews = []
		for review in reviews:
			series_reviews.append(pd.Series(review.items(), index=super().df.columns))
		super().df = super().df._append(reviews, ignore_index=True)
		self.export()
	
	def get_index(self) -> Index:
		return super().df.index

	def get_series(self, column: str) -> Series:
		return super().df[column]

	def get_reviews(self, *mask):
		return super().df.loc[mask]