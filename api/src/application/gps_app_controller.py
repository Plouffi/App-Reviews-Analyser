from flask import jsonify, request
from flask_classy import FlaskView, route

from config import CONFIG, ROOT_DIR
from src.domain.services.gps.gps_service import GPSService
from src.domain.services.scraper.scraper_service import ScraperService
from src.infrastructure.dataframe.impl.reviews_df import ReviewsDF
from src.infrastructure.sqlite.impl.gps_app_sqlite_repository import GPSAppSQLite

class GPSAppController(FlaskView):

	config: any
	gps_service: GPSService
	scraper: ScraperService
	reviews_df_repo: ReviewsDF
	gps_app_sqlite_repo: GPSAppSQLite

	def __init__(self) -> None:
		super().__init__()
		self.config = CONFIG
		self.reviews_df_repo = ReviewsDF(self.config, "reviews")
		self.gps_app_sqlite_repo = GPSAppSQLite(f"{ROOT_DIR}/{self.config['database']['ara']['path']}")
		self.gps_service = GPSService(self.config, self.reviews_df_repo, self.gps_app_sqlite_repo)
		self.scraper = ScraperService(self.config)

	@route('/search')
	def search(self):
		"""
			Method to search app on playstore
		"""
		search = request.args.get('search')
		
		try:
			return jsonify(self.scraper.search_app(search))
		except:
			return f"Error on '{super().route_base}/search' request", 500
		
	@route('/detail')
	def detail(self):
		"""
			Method to get app detail on playstore
		"""
		id = request.args.get('id')
		
		try:
			#TODO demander l'app detail pour toutes les langues/country pour avoir la somme du nombre de reviews
			return jsonify(self.scraper.app_detail(id))
		except:
			return f"Error on '{super().route_base}/detail' request", 500

	@route('/scraping')
	def scraping(self):
		"""
			Method to fetch reviews from the Playstore and store it
		"""
		id = request.args.get('id')
		
		try:
			self.gps_service.save_app(id)
			self.gps_service.save_reviews(id)
			return 'OK', 200
		except:
			return f"Error on '{super().route_base}/scraping' request", 500