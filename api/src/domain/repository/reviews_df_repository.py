from typing import Dict
from datetime import datetime as dt

class IReviewsDFRepository:
	
	def insert_reviews(self, reviews):
		"""
		Method to store data review in a Dataframe and export it to csv
			Parameters
			----------
			reviews : Lis(Dict)
				Array of dictionnary containing data review

		"""
		pass

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
		pass