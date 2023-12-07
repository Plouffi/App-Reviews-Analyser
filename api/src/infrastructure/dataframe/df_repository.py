from typing import List
import pandas as pd
from pandas import DataFrame
from abc import ABC, abstractmethod
from dependency_injector.providers import Configuration

class DFRepository(ABC):
	
	columns: List[str]
	root_dir: str

	def __init__(self, config: Configuration, root_dir: str):
		"""
			Parameters
			----------
			config : Dict
				Program's configuration.

		"""
		self.columns = config['dataframe']['reviews']
		self.df = pd.DataFrame(columns=self.columns)
		self.root_dir = root_dir

	def load(self, path_to_csv: str) -> DataFrame:
		"""
		Method to load reviews from csv file. Set up the dataframe's index on "at" column (publication date)
		"""
		try :
			self.df = pd.read_csv(f"{self.root_dir}{path_to_csv}")
			self.df = self.indexing(self.df)
			return self.df
		except FileNotFoundError:
			return self.get_df()

	@abstractmethod
	def indexing(self, df: DataFrame) -> DataFrame:
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
		df.to_csv(f"{self.root_dir}\\{export_path}", index=False)