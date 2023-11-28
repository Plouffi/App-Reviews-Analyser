from flask import request, Response
from flask_classy import FlaskView, route
from dependency_injector.wiring import Provide, inject

from application_container import ApplicationContainer
from src.application.response.a_response import TypeResponse
from src.application.response.impl.stats_response import StatsResponse
from src.application.response.impl.image_response import ImageResponse
from src.application.request.score_distribution_request import ScoreDistributionRequest
from src.application.request.means_request import MeansRequest
from src.application.request.stats_request import StatsRequest
from src.application.response.impl.stats_response import StatsResponse
from src.application.utils.application_utils import ApplicationUtils
from src.domain.services.i_analyser_service import IAnalyserService
from src.domain.services.i_plot_service import IPlotService


class AnalyserController(FlaskView):

	analyser_service: IAnalyserService
	plot_service: IPlotService

	@inject
	def __init__(self, 
							analyser_service: IAnalyserService = Provide[ApplicationContainer.analyser_service],
							plot_service: IPlotService = Provide[ApplicationContainer.plot_service]) -> None:
		super().__init__()
		self.analyser_service = analyser_service
		self.plot_service = plot_service

	@route('/scoreDistribution', methods=['POST'])
	def score_distribution(self):
		"""Compute score distribution from reviews data and returns it as a bar chart image
			---
			description: Get a gist
			responses:
				200:
					content:
						application/json:
							schema: GistSchema
			"""
		req = ScoreDistributionRequest(request)
		
		try:
			# computing stats
			score_distribution, review_distribution = self.analyser_service.score_distribution(req.app_id, req.date)

			# Convert plot to PNG image
			figure_plot_SD = self.plot_service.score_distribution(score_distribution, review_distribution, req.date)
			image_plot_SD = ApplicationUtils.get_image_from_plot(self.plot_service, figure_plot_SD)

			image_response = ImageResponse(image_plot_SD)
			return image_response.response(TypeResponse.PNG)
		except:
			return Response(response=f"Error on '{super().route_base}/scoreDistribution' request", status=500)

	@route('/means', methods=['POST'])
	def means(self):
		"""Compute means from reviews data and returns it as a graph image"""

		req = MeansRequest(request)

		try:
			# computing stats
			cumulative_mean, rolling_mean, rolling_sum = self.analyser_service.means_stats(req.app_id, req.time_delta, req.nb_ignore)

			# Convert plot to PNG image
			figure_plot_res = self.plot_service.means(cumulative_mean, rolling_mean, rolling_sum)
			image_plot_res = ApplicationUtils.get_image_from_plot(self.plot_service, figure_plot_res)
		
			image_response = ImageResponse(image_plot_res)
			return image_response.response(TypeResponse.PNG)
		except:
			return Response(response=f"Error on '{super().route_base}/means' request", status=500)
		
	@route('/stats', methods=['POST'])
	def overall_stats(self):
		"""Compute stats from reviews data and returns it as a JSON object"""
		req = StatsRequest(request)
		
		try:
			# computing stats
			means, nb_reviews = self.analyser_service.mean()
			review_with_mention, review_in_lang, review_with_mention_1star = self.analyser_service.mentions(req.lang, req.keywords)
			stats = StatsResponse(means, nb_reviews, review_with_mention, review_in_lang, review_with_mention_1star)
			
			# return stats
			return stats.response(TypeResponse.JSON)
		except:
			return Response(response=f"Error on '{super().route_base}/stats' request", status=500)