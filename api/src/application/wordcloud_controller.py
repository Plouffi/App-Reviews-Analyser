from flask import  jsonify, request, Response
from flask_classy import FlaskView, route
from dependency_injector.wiring import Provide, inject
import io

from application_container import ApplicationContainer
from src.application.request.words_request import WordsRequest
from src.domain.services.i_cloud_service import ICloudService
from src.domain.services.i_gps_service import IGPSService
from src.domain.services.i_make_image_service import IMakeImageService


class WordcloudController(FlaskView):

	cloud_service: ICloudService
	gps_service: IGPSService
	make_image_service: IMakeImageService

	@inject
	def __init__(self,
							gps_service: IGPSService = Provide[ApplicationContainer.gps_service],
							cloud_service: ICloudService = Provide[ApplicationContainer.cloud_service],
							make_image_service: IMakeImageService = Provide[ApplicationContainer.scraper_service]) -> None:
		super().__init__()
		self.gps_service = gps_service
		self.cloud_service = cloud_service
		self.make_image_service = make_image_service


	@route('/words', methods=['POST'])
	def words(self):
		"""Generate a list of top words from reviews app"""
		req = WordsRequest(request)
		
		try:
			reviews_before_fp = self.gps_service.get_reviews(req.app_id, req.start_date_1, req.end_date_1, req.lang, req.score)
			reviews_after_fp = self.gps_service.get_reviews(req.app_id, req.start_date_2, req.end_date_2, req.lang, req.score)
			self.cloud_service.load_reviews(req.alpha, req.n, [reviews_before_fp, reviews_after_fp])
			
			return jsonify(self.cloud_service.get_words())
		except:
			return Response(response=f"Error on '{super().route_base}/words' request", status=500)

	@route('/image', methods=['POST'])
	def wordcloud(self):
		"""Generate a wordcloud image from an array of words and frequencies."""
		words = request.get_json()['words']
		try:
			wordcloud = self.make_image_service.simple_image(words)

			# Convert plot to PNG image
			image = io.BytesIO()
			wordcloud.save(image, format='PNG')

			return Response(image.getvalue(), status=200, mimetype='image/png')
		except:
			return Response(response=f"Error on '{super().route_base}/image' request", status=500)