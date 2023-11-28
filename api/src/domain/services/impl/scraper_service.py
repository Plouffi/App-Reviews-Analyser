from typing import Dict, List
import numpy as np
from datetime import datetime as dt
from google_play_scraper import app
from google_play_scraper import Sort

from src.domain.services.i_scraper_service import IScraperService
from src.domain.services.utils.scraper_utils import reviews_all as gps_reviews
from src.domain.services.utils.scraper_utils import search as gps_search
from src.domain.model.gps_app import GPSApp
from src.domain.model.review import Review


class ScraperService(IScraperService):

	config: Dict

	def __init__(self, config: Dict):
		self.config = config

	def search_app(self, search: str) -> List[GPSApp]:
		return map(lambda a: GPSApp(a), gps_search(search, lang='en', country='us', n_hits=self.config['nSearchResult']))
	
	def app_detail(self, app_id: str) -> GPSApp:
		return GPSApp(app(app_id=app_id, lang='en', country='us')) #TODO: handle language

	def get_reviews(self, app_id: str, date: dt) -> List[Review]:

		def extract_review(review_to_extract: Dict, language_to_add: str) -> Review:
			review_to_extract['language'] = language_to_add
			return Review(review_to_extract)

		reviews = []

		# there is a weird glitch in data for DK, FI and PR country where they have all the same HUGE number of reviews 
		# I remove them from the list to approach the total number of reviews (still not perfect)
		languages = np.unique(list(map(lambda l: l['lang'], self.config['languages'])))
		for l in languages:
			res = gps_reviews(
				app_id,
				date,
				lang=l,
				country='US', #doesnt matter 
				sleep_milliseconds=100,
				sort=Sort.NEWEST
			)
			res = map(lambda review : extract_review(review, 'en'), res) #TODO: handle language
			reviews = [*reviews, *res]
		return reviews