from typing import List
import pandas as pd
from pandas import DataFrame, Index, Series

from src.infrastructure.dataframe.df_repository import DFRepository
from src.domain.repository.reviews_repository import IReviewsRepository
from src.domain.model.review import Review

class ReviewsDF(DFRepository, IReviewsRepository):

	def indexing(self, df: DataFrame):
		df["at"] = pd.to_datetime(df["at"])
		df = df.set_index("at")
		df = df.sort_values("at", ascending=True)
		
	def insert(self, reviews, path_to_csv: str):
		df = super().get_df()
		series_reviews = []
		for review in reviews:
			series_reviews.append(pd.Series(review.items(), index=df.columns))
		df = df._append(reviews, ignore_index=True)
		self.export(path_to_csv)
	
	def get_df(self, path_to_csv: str) -> DataFrame:
		return super().load(path_to_csv) if path_to_csv is not None else super().get_df()
	
	def get_index(self, df: DataFrame) -> Index:
		return df.index

	def get_series(self, df: DataFrame, column: str) -> Series:
		return df[column]

	def get(self, df: DataFrame, *mask) -> List[Review]:
		return df.loc[mask]