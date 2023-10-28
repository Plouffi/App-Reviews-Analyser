from typing import List, Any
from datetime import datetime as dt
from src.Model.gps_app import App
from src.Scraper.scraper_utils import reviews_all as gps_reviews
from src.Scraper.scraper_utils import search as gps_search
from google_play_scraper import app
from google_play_scraper import Sort



class Scraper:

	def __init__(self, config):
		self.config = config

	def search_app(self, search: str) -> List[Any]:
		result = []
		apps = map(lambda a: App(a), gps_search(search, lang="en", country='us', n_hits=self.config['n_search_result']))
		result += map(lambda a : a.shorten(), apps)
		return result
	
	def app_detail(self, id: str) -> Any:
		gps_app = app(app_id=id, lang='en', country='us') # default info
		for language in self.config['languages']:
			if language['country'] != 'us':
				detail_app = app(app_id=id, lang=language['lang'], country=language['country'])
				gps_app['reviews'] += detail_app['reviews'] # We sum reviews to have the total
		return gps_app

	def get_reviews(self, date):
		def clear_data(reviews_to_clear, language_to_add):
			for review in reviews_to_clear:
				del review['userImage']
				del review['userImage']
				del review['replyContent']
				del review['repliedAt']
				review['language'] = language_to_add
			return reviews_to_clear

		reviews = []

		for language in self.config['languages']:
			res = gps_reviews(
				self.config['app'],
				dt.strptime(date, '%Y-%m-%d %I:%M%p'),
				lang=language['lang'],
				country=language['country'],
				sort=Sort.NEWEST
			)
			res = clear_data(res, language)
			reviews = [*reviews, *res]
		print('Total reviews fetched: %d', len(reviews))
		return reviews
