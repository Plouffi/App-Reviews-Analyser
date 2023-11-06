from flask import  request, Response
from flask_classy import FlaskView, route
import io
import json

from src.application.cloud.cloud_service import CloudService
from src.application.gps.gps_service import GPSService
from src.infrastructure.dataframe.impl.reviews_df import ReviewsDF
import src.application.image.make_image as make_image


class WordcloudController(FlaskView):

	config: any
	cloud: CloudService
	gps_service: GPSService
	reviews_df_repo: ReviewsDF

	def __init__(self) -> None:
		super().__init__()
		with open('./resources/config.json', errors='replace') as f:
			self.config = json.load(f)
			self.cloud = CloudService()
			self.reviews_df_repo = ReviewsDF(self.config, "reviews")
			self.gps_service = GPSService(self.config, self.reviews_df_repo)


	@route('/words', methods=['POST'])
	def words(self):
		"""
			Method to generate a word cloud. Images are save in "resources" directory.
		"""
		alpha = float(request.get_json().get('alpha', 10))
		n = int(request.get_json().get('n', 2))
		start_date_1 = request.get_json()['start1']
		start_date_2 = request.get_json()['start2']
		end_date_1 = request.get_json()['end1']
		end_date_2 = request.get_json()['end2']
		lang = str(request.get_json()['lang'])
		score = int(request.get_json().get('score', 0))
		
		try:
			reviews_before_fp = self.gps_service.get_reviews(start_date_1, end_date_1, lang, score)
			reviews_after_fp = self.gps_service.get_reviews(start_date_2, end_date_2, lang, score)
			self.cloud.load_reviews(alpha, n, [reviews_before_fp, reviews_after_fp])
			return self.cloud.get_words(), 200
		except:
			return f"Error on '{super().route_base}/words' request", 500

	@route('/image', methods=['POST'])
	def wordcloud(self):
		"""
			Method to generate a word cloud from an array of words and frequencies.
		"""
		words = request.get_json()['words']
		try:
			wordcloud = make_image.simple_image(words)

			# Convert plot to PNG image
			image = io.BytesIO()
			wordcloud.save(image, format='PNG')

			return Response(image.getvalue(), mimetype='image/png'), 200
		except:
			return f"Error on '{super().route_base}/image' request", 500