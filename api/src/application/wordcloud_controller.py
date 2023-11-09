from typing import Dict
from flask import  request, Response
from flask_classy import FlaskView, route
from dependency_injector.wiring import Provide, inject
import io

from config import CONFIG
from application_container import ApplicationContainer
from src.domain.services.i_cloud_service import ICloudService
from src.domain.services.i_gps_service import IGPSService
from src.domain.services.i_make_image_service import IMakeImageService

class WordcloudController(FlaskView):

	config: Dict
	cloud_service: ICloudService
	gps_service: IGPSService
	make_image_service: IMakeImageService

	@inject
	def __init__(self,
							gps_service: IGPSService = Provide[ApplicationContainer.gps_service],
							cloud_service: ICloudService = Provide[ApplicationContainer.cloud_service],
							make_image_service: IMakeImageService = Provide[ApplicationContainer.scraper_service]) -> None:
		super().__init__()
		self.config = CONFIG
		self.gps_service = gps_service
		self.cloud_service = cloud_service
		self.make_image_service = make_image_service


	@route('/words', methods=['POST'])
	def words(self):
		"""
			Method to generate a word cloud. Images are save in "resources" directory.
		"""
		app_id = str(request.get_json()['app_id'])
		alpha = float(request.get_json().get('alpha', 10))
		n = int(request.get_json().get('n', 2))
		start_date_1 = request.get_json()['start1']
		start_date_2 = request.get_json()['start2']
		end_date_1 = request.get_json()['end1']
		end_date_2 = request.get_json()['end2']
		lang = str(request.get_json()['lang'])
		score = int(request.get_json().get('score', 0))
		
		try:
			reviews_before_fp = self.gps_service.get_reviews(app_id, start_date_1, end_date_1, lang, score)
			reviews_after_fp = self.gps_service.get_reviews(app_id, start_date_2, end_date_2, lang, score)
			self.cloud_service.load_reviews(alpha, n, [reviews_before_fp, reviews_after_fp])
			return self.cloud_service.get_words(), 200
		except:
			return f"Error on '{super().route_base}/words' request", 500

	@route('/image', methods=['POST'])
	def wordcloud(self):
		"""
			Method to generate a word cloud from an array of words and frequencies.
		"""
		words = request.get_json()['words']
		try:
			wordcloud = self.make_image_service.simple_image(words)

			# Convert plot to PNG image
			image = io.BytesIO()
			wordcloud.save(image, format='PNG')

			return Response(image.getvalue(), mimetype='image/png'), 200
		except:
			return f"Error on '{super().route_base}/image' request", 500