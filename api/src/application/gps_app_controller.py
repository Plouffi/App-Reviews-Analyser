from typing import Dict
from flask import jsonify, request, Response
from flask_classy import FlaskView, route
from dependency_injector.wiring import Provide, inject

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
		self.gps_service = gps_service
		self.scraper_service = scraper_service

	@route('/search')
	def search(self):
		"""Search app on playstore"""
		search = request.args.get('search')
		try:
			return jsonify(self.scraper_service.search_app(search))
		except:
			return Response(response=f"Error on '{super().route_base}/search' request", status=500)
		
	@route('/detail')
	def detail(self):
		"""Get app detail on playstore"""
		id = request.args.get('id')
		try:
			#TODO demander l'app detail pour toutes les langues/country pour avoir la somme du nombre de reviews
			return jsonify(self.scraper_service.app_detail(id))
		except:
			return Response(response=f"Error on '{super().route_base}/detail' request", status=500)

	@route('/scraping')
	def scraping(self):
		"""Fetch reviews from the Playstore and store it"""
		id = request.args.get('id')
		try:
			self.gps_service.save_app(id)
			self.gps_service.save_reviews(id)
			return Response(response='OK', status=200)
		except:
			return Response(response=f"Error on '{super().route_base}/scraping' request", status=500)