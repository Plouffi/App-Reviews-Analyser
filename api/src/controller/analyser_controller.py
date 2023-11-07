from flask import request, Response
from flask_classy import FlaskView, route
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io

from config import CONFIG, ROOT_DIR
from src.application.analyser.analyser_service import AnalyserService
from src.application.plot.plot_service import PlotService
from src.infrastructure.sqlite.impl.gps_app_sqlite_repository import GPSAppSQLite
from src.infrastructure.dataframe.impl.reviews_df import ReviewsDF


class AnalyserController(FlaskView):

	config: any
	analyser: AnalyserService
	plot: PlotService
	gps_app_sqlite_repository: GPSAppSQLite
	reviews_df_repo: ReviewsDF

	def __init__(self) -> None:
		super().__init__()
		self.config = CONFIG
		self.reviews_df_repo = ReviewsDF(self.config, "reviews")
		self.gps_app_sqlite_repository = GPSAppSQLite(f"{ROOT_DIR}/{self.config['dataframe']['reviews']['path']}")
		self.analyser = AnalyserService(self.config, self.gps_app_sqlite_repository, self.reviews_df_repo)
		self.plot = PlotService(self.config)

	@route('/scoreDistribution', methods=['POST'])
	def score_distribution(self):
		"""
			Method to compute scoren distribution from reviews data
		"""
		app_id = str(request.get_json()['app_id'])
		date = request.get_json().get('date', None)
		
		try:
			# computing stats
			score_distribution, review_distribution = self.analyser.score_distribution(app_id, date)

			# Convert plot to PNG image
			figure_plot_SD = self.plot.score_distribution(score_distribution, review_distribution, date)
			image_plot_SD = io.BytesIO()
			FigureCanvas(figure_plot_SD).print_png(image_plot_SD)
			self.plot.refresh()
			
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
			cumulative_mean, rolling_mean, rolling_sum = self.analyser.means_stats(app_id, time_delta, nb_ignore)
			means = {
				'Cumulative mean': cumulative_mean,
				'Rolling average (1 month)': rolling_mean,
				'Rolling sum of reviews (1 month)': rolling_sum
			}

			# Convert plot to PNG image
			figure_plot_res = self.plot.means(means)
			image_plot_res = io.BytesIO()
			FigureCanvas(figure_plot_res).print_png(image_plot_res)
			self.plot.refresh()
		
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
			means, nb_reviews = self.analyser.mean()
			review_with_mention, review_in_lang, review_with_mention_1star = self.analyser.mentions(lang, keywords)
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