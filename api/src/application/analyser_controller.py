from typing import Dict
from flask import request, Response
from flask_classy import FlaskView, route
from dependency_injector.wiring import Provide, inject
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io

from config import CONFIG
from application_container import ApplicationContainer
from src.domain.services.i_analyser_service import IAnalyserService
from src.domain.services.i_plot_service import IPlotService


class AnalyserController(FlaskView):

	config: Dict
	analyser_service: IAnalyserService
	plot_service: IPlotService

	@inject
	def __init__(self, 
							analyser_service: IAnalyserService = Provide[ApplicationContainer.analyser_service],
							plot_service: IPlotService = Provide[ApplicationContainer.plot_service]) -> None:
		super().__init__()
		self.config = CONFIG
		self.analyser_service = analyser_service
		self.plot_service = plot_service

	@route('/scoreDistribution', methods=['POST'])
	def score_distribution(self):
		"""
			Method to compute scoren distribution from reviews data
		"""
		app_id = str(request.get_json()['app_id'])
		date = request.get_json().get('date', None)
		
		try:
			# computing stats
			score_distribution, review_distribution = self.analyser_service.score_distribution(app_id, date)

			# Convert plot to PNG image
			figure_plot_SD = self.plot_service.score_distribution(score_distribution, review_distribution, date)
			image_plot_SD = io.BytesIO()
			FigureCanvas(figure_plot_SD).print_png(image_plot_SD)
			self.plot_service.refresh()
			
			return Response(image_plot_SD.getvalue(), mimetype='image/png')

		except:
			return f"Error on '{super().route_base}/scoreDistribution' request", 500

	@route('/means', methods=['POST'])
	def means(self):
		"""
			Method to compute statistics from reviews data
		"""
		app_id = str(request.get_json()['app_id'])
		time_delta = int(request.get_json().get('timeDelta', 30))
		nb_ignore = int(request.get_json().get('ignore', 0))

		try:
			# computing stats
			cumulative_mean, rolling_mean, rolling_sum = self.analyser_service.means_stats(app_id, time_delta, nb_ignore)
			means = {
				'Cumulative mean': cumulative_mean,
				'Rolling average (1 month)': rolling_mean,
				'Rolling sum of reviews (1 month)': rolling_sum
			}

			# Convert plot to PNG image
			figure_plot_res = self.plot_service.means(means)
			image_plot_res = io.BytesIO()
			FigureCanvas(figure_plot_res).print_png(image_plot_res)
			self.plot_service.refresh()
		
			return Response(image_plot_res.getvalue(), mimetype='image/png')
		except:
			return f"Error on '{super().route_base}/means' request", 500
		
	@route('/stats', methods=['POST'])
	def overall_stats(self):
		"""
			Method to compute statistics from reviews data
		"""
		app_id = str(request.get_json()['app_id'])
		lang = str(request.get_json()['lang'])
		keywords = request.get_json()['keywords']
		
		try:
			# computing stats
			means, nb_reviews = self.analyser_service.mean()
			review_with_mention, review_in_lang, review_with_mention_1star = self.analyser_service.mentions(lang, keywords)
			stats = {
				'means': means,
				'nb_reviews': nb_reviews,
				'review_in_lang': len(review_in_lang),
				'review_with_mention': len(review_with_mention),
				'review_with_mention_1star': len(review_with_mention_1star)
			}
			
			# return stats
			return stats, 200

		except:
			return f"Error on '{super().route_base}/stats' request", 500