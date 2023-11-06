from typing import Any, List
from datetime import datetime

class GPSApp:
    """
		Class to representing an app from the Google Play Store
		...
		Attributes
		----------
		id : str
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
        realInstalls: str
        totalReviews: int
        reviews: int
        url: str
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


    def __init__(self, gps_app):
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

    def shorten(self) -> Any:
        """
            Method shortening detail's app 
        """
        return {
			'id': self.id,
			'title': self.title,
			'icon': self.icon,
		}
    
    def formatDate(self, date: str, lang: str) -> datetime:
        """
            Method to format the released date
        """
        return datetime.strptime(f"{date} 00:00", '%b %d, %Y %H:%M')
