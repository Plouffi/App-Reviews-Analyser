from typing import List

class App:
    """
		Class to representing an app from the Google Play Store
		...
		Attributes
		----------
		id : str
        title: str
        icon: str
        score: float
        genre: str
        price: float
        currency: str
        free: bool
        description: str
        descriptionHTML: str
        developer: str
        installs: str
	"""
    id: str
    title: str
    icon: str
    score: float
    genre: str
    price: float
    currency: str
    free: bool
    description: str
    descriptionHTML: str
    developer: str
    installs: str

    def __init__(self, gps_app):
        self.id = gps_app['appId'] if 'appId' in gps_app else ''
        self.title = gps_app['title'] if 'title' in gps_app else ''
        self.icon = gps_app['icon'] if 'icon' in gps_app else ''
        self.score = gps_app['score'] if 'score' in gps_app else ''
        self.genre = gps_app['genre'] if 'genre' in gps_app else ''
        self.price = gps_app['price'] if 'price' in gps_app else ''
        self.free = gps_app['free'] if 'free' in gps_app else ''
        self.currency = gps_app['currency'] if 'currency' in gps_app else ''
        self.description = gps_app['description'] if 'description' in gps_app else ''
        self.descriptionHTML = gps_app['descriptionHTML'] if 'descriptionHTML' in gps_app else ''
        self.developer = gps_app['developer'] if 'developer' in gps_app else ''
        self.installs = gps_app['installs'] if 'installs' in gps_app else ''

    def shorten(self): 
        """
            Method shortening detail's app 
        """
        return {
			'id': self.id,
			'title': self.title,
			'icon': self.icon,
		}