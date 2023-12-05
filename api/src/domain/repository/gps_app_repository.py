from typing import Tuple
from abc import ABC, abstractmethod
from src.domain.model.gps_app import GPSApp

class IGPSAppRepository(ABC):
  
	@abstractmethod
	def insert(self, gps_app: GPSApp):
		"""
		Insert a gps_app into GPS_APP table
		"""
		pass

	@abstractmethod
	def get(self, app_id: str):
		"""
		Return the corresponding GPSApp from targeted app_id
		"""
		pass

	@abstractmethod
	def list(self):
		"""
		Return all GPS stored
		"""
		pass

	@abstractmethod
	def update(self, app_id: str, *fieldsValue: Tuple[str, str]):
		"""
		Update the selected fields of an app
		"""
		pass

	@abstractmethod
	def commit(self): 
		pass
	
	@abstractmethod
	def rollback(self): 
		pass