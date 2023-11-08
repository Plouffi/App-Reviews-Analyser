from typing import Dict
from datetime import datetime

class ExportStatus:
	"""Enum to represente the exporting status of reviews
	----------"""
	NO_EXPORT: 0
	EXPORTING: 1
	EXPORTED: 2

class GPSApp:
	"""Class representing an app from the Google Playstore
	----------
	Attributes:
	id (str)
	title (str)
	icon (str)
	headerImage (str)
	video (str)
	videoImage (str)
	screenshots (List[str])
	score (float)
	genre (str)
	categories (List[str])
	price (float)
	currency (str)
	free (bool)
	summary (str)
	description (str)
	descriptionHTML (str)
	version (str)
	released (datetime)
	developer (str)
	developerWebsite (str)
	installs (str)
	realInstalls (str)
	totalReviews (int)
	reviews (int)
	url (str)
	exportPath (str)
	exportDate (datetime)
	exporting (ExportStatus)
	"""

	id: str
	title: str
	icon: str
	headerImage: str
	video: str
	videoImage: str
	screenshots: list[str]
	score: float
	genre: str
	categories: list[str] 
	price: float
	currency: str
	free: bool
	summary: str
	description: str
	descriptionHTML: str
	version: str
	released: datetime
	developer: str
	developerWebsite: str
	installs: str
	realInstalls: int
	totalReviews: int
	reviews: int
	url: str
	exportPath: str
	exportDate: datetime
	exportStatus: ExportStatus


	def __init__(self, gps_app: Dict) -> None :
		self.id = gps_app['appId'] if 'appId' in gps_app else ''
		self.title = gps_app['title'] if 'title' in gps_app else ''
		self.icon = gps_app['icon'] if 'icon' in gps_app else ''
		self.headerImage = gps_app['headerImage'] if 'headerImage' in gps_app else ''
		self.video = gps_app['video'] if 'video' in gps_app else ''
		self.videoImage = gps_app['videoImage'] if 'videoImage' in gps_app else ''
		self.screenshots = gps_app['screenshots'] if 'screenshots' in gps_app else []
		self.score = gps_app['score'] if 'score' in gps_app else 0
		self.genre = gps_app['genre'] if 'genre' in gps_app else ''
		self.categories = list(map(lambda c : c['name'], gps_app['categories']))  if 'categories' in gps_app else []
		self.price = gps_app['price'] if 'price' in gps_app else 0
		self.free = gps_app['free'] if 'free' in gps_app else ''
		self.currency = gps_app['currency'] if 'currency' in gps_app else ''
		self.summary = gps_app['summary'] if 'summary' in gps_app else ''
		self.description = gps_app['description'] if 'description' in gps_app else ''
		self.descriptionHTML = gps_app['descriptionHTML'] if 'descriptionHTML' in gps_app else ''
		self.version = gps_app['version'] if 'version' in gps_app else ''
		self.released = self.formatDate(gps_app['released'], 'en') if 'released' in gps_app else '' #TODO: handle language
		self.developer = gps_app['developer'] if 'developer' in gps_app else ''
		self.developerWebsite = gps_app['developerWebsite'] if 'developerWebsite' in gps_app else ''
		self.installs = gps_app['installs'] if 'installs' in gps_app else ''
		self.realInstalls = gps_app['realInstalls'] if 'realInstalls' in gps_app else ''
		self.totalReviews = gps_app['ratings'] if 'ratings' in gps_app else 0
		self.reviews = gps_app['reviews'] if 'reviews' in gps_app else 0
		self.url = gps_app['url'] if 'url' in gps_app else ''
		self.exportPath = gps_app['exportPath'] if 'exportPath' in gps_app else ""
		self.exportDate = gps_app['exportDate'] if 'exportDate' in gps_app else None
		self.exportStatus = gps_app['exportStatus'] if 'exportStatus' in gps_app else ExportStatus.NO_EXPORT

	def shorten(self) -> Dict:
		"""Shorten app detail.
		----------
		Returns:
		Any: the shorten app
		"""
		return {
			'id': self.id,
			'title': self.title,
			'icon': self.icon
		}

	def formatDate(self, date: str, lang: str) -> datetime:
		"""Format the released date.
		----------
		Parameters:
		date (str): the date to format.
		lang (str): Determines the location for the date format
		----------
		Returns:
		datetime: The formatted date
		"""
		return datetime.strptime(f"{date} 00:00", '%b %d, %Y %H:%M')
