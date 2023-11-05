from flask import jsonify, request
from flask_classy import FlaskView, route
import json

from src.application.scraper.scraper import Scraper


class GPSAppController(FlaskView):

	config: any
	scraper: Scraper

	def __init__(self) -> None:
		super().__init__()
		with open('./ressources/config.json', errors='replace') as f:
			self.config = json.load(f)
			self.scraper = Scraper(self.config)

	@route('/search')
	def search(self):
		"""
			Method to search app on playstore
		"""
		search = request.args.get('search')
		
		try:
			return jsonify(self.scraper.search_app(search))

		except FileNotFoundError:
			return f"File '{self.config['export_path']}' not found. Launch scraping process to create it", 500
		
	@route('/detail')
	def detail(self):
		"""
			Method to get app detail on playstore
		"""
		id = request.args.get('id')
		
		try:
			
			#TODO demander l'app detail pour toutes les langues/country pour avoir la somme du nombre de reviews
			return self.scraper.app_detail(id).__dict__

		except FileNotFoundError:
			return f"File '{self.config['export_path']}' not found. Launch scraping process to create it", 500

	@route('/scraping')
	def scraping(self):
		"""
			Method to fetch reviews from the Playstore and store it
		"""
		id = request.args.get('id')
		
		try:
			# TODO: save app and reviews with another service into DB
			app = self.scraper.app_detail(id)
			reviews = self.scraper.get_reviews(app.released)
			self.scraper.save_reviews(reviews=reviews)

			return 'OK', 200
		except FileNotFoundError:
			return f"File '{self.config['export_path']}' not found. Launch scraping process to create it", 500