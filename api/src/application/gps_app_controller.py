from typing import Dict
from flask import jsonify, request, Response
from flask_classy import FlaskView, route
from dependency_injector.wiring import Provide, inject

from application_container import ApplicationContainer
from src.application.response.a_response import TypeResponse
from src.application.response.impl.scraping_response import ScrapingResponse
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
			result = []
			result += map(lambda a : a.serialize_short(), self.scraper_service.search_app(search))
			return jsonify(result)
		except Exception as e:
			print(e)
			return Response(response=f"Error on '{super().route_base}/search' request", status=500)
		
	@route('/apps')
	def search(self):
		"""Return the list of scrapped app"""
		try:
			result = []
			lista = self.gps_service.get_apps()
			result += map(lambda a : a.serialize_short(), lista)
			return jsonify(result)
		except Exception as e:
			print(e)
			return Response(response=f"Error on '{super().route_base}/apps' request", status=500)
		
	@route('/detail')
	def detail(self):
		"""Get app detail on playstore"""
		id = request.args.get('id')
		try:
			#TODO demander l'app detail pour toutes les langues/country pour avoir la somme du nombre de reviews
			return jsonify(self.scraper_service.app_detail(id).serialize())
		except Exception as e:
			print(e)
			return Response(response=f"Error on '{super().route_base}/detail' request", status=500)

	@route('/scraping')
	def scraping(self):
		"""Fetch reviews from the Playstore and store it"""
		id = request.args.get('id')
		try:
			self.gps_service.save_app(id)
			self.gps_service.save_reviews(id)
			return ScrapingResponse(msg='OK').response(TypeResponse.JSON)
		except Exception as e:
			print(e)
			return Response(response=f"Error on '{super().route_base}/scraping' request", status=500)