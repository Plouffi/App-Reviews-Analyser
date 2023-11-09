from typing import Dict
from flask import jsonify, request
from flask_classy import FlaskView, route
from dependency_injector.wiring import Provide, inject


from config import CONFIG
from application_container import ApplicationContainer
from src.domain.services.i_gps_service import IGPSService
from src.domain.services.i_scraper_service import IScraperService

class GPSAppController(FlaskView):

	config: Dict
	gps_service: IGPSService
	scraper_service: IScraperService

	@inject
	def __init__(self, 
							gps_service: IGPSService = Provide[ApplicationContainer.gps_service],
							scraper_service: IScraperService = Provide[ApplicationContainer.scraper_service]) -> None:
		super().__init__()
		self.config = CONFIG
		self.gps_service = gps_service
		self.scraper_service = scraper_service

	@route('/search')
	def search(self):
		"""
			Method to search app on playstore
		"""
		search = request.args.get('search')
		
		try:
			return jsonify(self.scraper_service.search_app(search))
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
			return jsonify(self.scraper_service.app_detail(id))
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