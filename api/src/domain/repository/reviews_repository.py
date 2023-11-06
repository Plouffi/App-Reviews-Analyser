from abc import ABC, abstractmethod
from pandas import Index, Series

class IReviewsRepository(ABC):
	
	@abstractmethod
	def insert(self, reviews):
		"""
		Method to store data review in a Dataframe and export it to csv
			Parameters
			----------
			reviews : Lis(Dict)
				Array of dictionnary containing data review

		"""
		pass

	@abstractmethod
	def get_index(self) -> Index:
		"""
		Return the Series corresponding to the dataframe index
		"""
		pass

	@abstractmethod
	def get_series(self, column: str) -> Series:
		"""
		Return a Series corresponding to the targeted column
		"""
		pass

	@abstractmethod
	def get(self, *mask):
		"""
		Return result from the masks request
		"""
		pass
