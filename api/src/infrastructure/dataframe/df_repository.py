import pandas as pd
from pandas import DataFrame
from abc import ABC, abstractmethod

class DFRepository(ABC):
	
	df: DataFrame

	def __init__(self, config, schema):
		"""
			Parameters
			----------
			config : Dict
				Program's configuration.

		"""
		columns = config["dataframe"][schema]
		self.df = pd.DataFrame(columns=columns)
		self.config = config

	def load(self, path_to_csv: str) -> DataFrame:
		"""
		Method to load reviews from csv file. Set up the dataframe's index on "at" column (publication date)
		"""
		self.df = pd.read_csv(path_to_csv)
		self.indexing()
		return self.get_df()

	@abstractmethod
	def indexing(self):
		"""
		Method to set up the index on records
		"""
		pass

	def get_df(self) -> DataFrame:
		"""
		Return the Dataframe
		"""
		return self.df
	
	def export(self, path_to_csv: str):
		"""
		Method to export reviews in csv.
		"""
		self.df.to_csv(path_to_csv, index=False)