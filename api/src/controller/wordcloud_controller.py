from flask import  request, Response
from flask_classy import FlaskView, route
import io
import json

from src.application.cloud.cloud import Cloud
from src.domain.DataManager.data_manager import DataManager
import src.application.image.make_image as make_image


class WordcloudController(FlaskView):

	config: any
	

	def __init__(self) -> None:
		super().__init__()
		with open('./ressources/config.json', errors='replace') as f:
			self.config = json.load(f)


	@route('/words', methods=['POST'])
	def words(self):
		"""
			Method to generate a word cloud. Images are save in "ressources" directory.
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
			reviews_before_fp = dm.get_reviews_as_dict(start_date=start_date_1, end_date=end_date_1, language=lang, score=score)
			reviews_after_fp = dm.get_reviews_as_dict(start_date=start_date_2, end_date=end_date_2, language=lang, score=score)
			cloud = Cloud(alpha=alpha, n=n)
			cloud.load_reviews(reviews_before_fp, reviews_after_fp)
			return cloud.get_words()

		except FileNotFoundError:
			print(f"File '{self.config['export_path']}' not found. Please check provided path is a valid path.")

	@route('/image', methods=['POST'])
	def wordcloud(self):
		"""
			Method to generate a word cloud from an array of words and frequencies.
		"""
		words = request.get_json()['words']
		wordcloud = make_image.simple_image(words)

		# Convert plot to PNG image
		image = io.BytesIO()
		wordcloud.save(image, format='PNG')

		return Response(image.getvalue(), mimetype='image/png')