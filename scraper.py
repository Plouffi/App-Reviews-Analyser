from scraper_utils import reviews as gps_r
from google_play_scraper import Sort
from datetime import datetime as dt


class Scraper:

	def __init__(self, config):
		self.config = config

	def get_reviews(self, date):
		return self.get_reviews_from_gps(date)

	def get_reviews_from_gps(self, date):
		def clear_data(reviews_to_clear, language_to_add):
			for review in reviews_to_clear:
				del review["userImage"]
				review["language"] = language_to_add
			return reviews_to_clear

		reviews = []

		for language in self.config["languages"]:
			res = gps_r(self.config["app"], lang=language, sort=Sort.NEWEST, date=dt.strptime(date, "%Y-%m-%d %I:%M%p"))
			res = clear_data(res, language)
			reviews = [*reviews, *res]
			print(language + ": %d reviews fetched" % len(res))
		print("Total reviews fetched: %d", len(reviews))
		return reviews
