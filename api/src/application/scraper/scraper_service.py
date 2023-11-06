from typing import List, Any
import numpy as np
from google_play_scraper import app
from google_play_scraper import Sort

from src.application.scraper.scraper_utils import reviews_all as gps_reviews
from src.application.scraper.scraper_utils import search as gps_search
from src.domain.model.gps_app import GPSApp


class ScraperService:

	def __init__(self, config):
		self.config = config

	def search_app(self, search: str) -> List[Any]:
		result = []
		apps = map(lambda a: GPSApp(a), gps_search(search, lang="en", country='us', n_hits=self.config['n_search_result']))
		result += map(lambda a : a.shorten(), apps)
		return result
	
	def app_detail(self, id: str) -> GPSApp:
		return GPSApp(app(app_id=id, lang='en', country='us')) #TODO: handle language

	def get_reviews(self, date):

		def clear_data(reviews_to_clear, language_to_add):
			for review in reviews_to_clear:
				del review['userImage']
				del review['replyContent']
				del review['repliedAt']
				review['language'] = language_to_add
			return reviews_to_clear

		reviews = []

		# there is a weird glitch in data for DK, FI and PR country where they have all the same HUGE number of reviews 
		# I remove them from the list to approach the total number of reviews (still not perfect)
		languages = np.unique(list(map(lambda l: l['lang'], self.config['languages'])))
		for l in languages:
			res = gps_reviews(
				self.config['app'],
				date,
				lang=l,
				country="US", #doesnt matter 
				sleep_milliseconds=100,
				sort=Sort.NEWEST
			)
		res = clear_data(res, 'en')
		reviews = [*reviews, *res]
		print('Total reviews fetched: %d', len(reviews))
		return reviews