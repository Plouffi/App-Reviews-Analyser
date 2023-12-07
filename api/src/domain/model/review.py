from typing import Dict
from datetime import datetime

class Review:
	"""Class representing a review of an app from the Google Playstore
	----------
	Attributes:
	username (str)
	content (str)
	score (int)
	thumbsUpCount (int)
	reviewCreatedVersion (datetime)
	at (datetime)
	language (str)
	"""
	username: str
	content: str
	score: int
	thumbsUpCount: int
	reviewCreatedVersion: datetime
	at: datetime
	language: str

	def __init__(self, review: Dict) -> None:
		"""""" 
		self.username = review['username'] if 'username' in review else ''
		self.content = review['content'] if 'content' in review else ''
		self.score = review['score'] if 'score' in review else 1
		self.thumbsUpCount = review['thumbsUpCount'] if 'thumbsUpCount' in review else 0
		self.reviewCreatedVersion = review['reviewCreatedVersion'] if 'reviewCreatedVersion' in review else None
		self.at = review['at'] if 'at' in review else None
		self.language = review['language'] if 'language' in review else ''

	def serialize(self) -> Dict:
		"""Serialize the review.
		----------
		Returns:
		Dict: serialized review
		"""
		return {
			'username': self.username,
			'content': self.content,
			'score': self.score,
			'thumbsUpCount': self.thumbsUpCount,
			'reviewCreatedVersion': self.reviewCreatedVersion,
			'at': self.at,
			'language': self.language
		}