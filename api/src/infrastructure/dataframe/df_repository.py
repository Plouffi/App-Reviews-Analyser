from typing import List
import pandas as pd
from pandas import DataFrame
from abc import ABC, abstractmethod

class DFRepository(ABC):
	
	columns: List[str]
	df: DataFrame

	def __init__(self, config, schema):
		"""
			Parameters
			----------
			config : Dict
				Program's configuration.

		"""
		self.columns = config["dataframe"][schema]
		self.df = pd.DataFrame(columns=self.columns)
		self.config = config

	def load(self, path_to_csv: str) -> DataFrame:
		"""
		Method to load reviews from csv file. Set up the dataframe's index on "at" column (publication date)
		"""
		try :
			df = pd.read_csv(path_to_csv)
			self.indexing(df)
			return df
		except FileNotFoundError:
			return self.get_df()

	@abstractmethod
	def indexing(self, df: DataFrame):
		"""
		Method to set up the index on records
		"""
		pass

	def get_df(self) -> DataFrame:
		"""
		Return a new Dataframe
		"""
		return pd.DataFrame(columns=self.columns)
	
	def export(self, df: DataFrame, export_path: str):
		"""
		Method to export reviews in csv.
		"""
		df.to_csv(export_path, index=False)