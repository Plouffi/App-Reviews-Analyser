from abc import ABC, abstractmethod
from pandas import DataFrame, Index, Series

class IReviewsRepository(ABC):
	
	@abstractmethod
	def insert(self, reviews, export_path: str):
		"""
		Method to store data review in a Dataframe and export it to csv
			Parameters
			----------
			reviews : Lis(Dict)
				Array of dictionnary containing data review
			export_path: str
				Path to store data into csv
		"""
		pass

	@abstractmethod
	def get_df(self, path_to_csv: str) -> DataFrame:
		"""
		Return a Dataframe from csv or a new Dataframe if file is not found
		"""
		pass

	@abstractmethod
	def get_index(self, df: DataFrame) -> Index:
		"""
		Return the Series corresponding to the dataframe index
		"""
		pass

	@abstractmethod
	def get_series(self, df: DataFrame, column: str) -> Series:
		"""
		Return a Series corresponding to the targeted column
		"""
		pass

	@abstractmethod
	def get(self, df: DataFrame, *mask):
		"""
		Return result from the masks request
		"""
		pass
