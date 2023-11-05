from flask import request, Response
from flask_classy import FlaskView, route
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import json

from src.domain.analyser.analyser import Analyser
from src.domain.plot.plot import Plot


class AnalyserController(FlaskView):

	config: any
	analyser: Analyser

	def __init__(self) -> None:
		super().__init__()
		with open('./ressources/config.json', errors='replace') as f:
			self.config = json.load(f)
			self.analyser = Analyser(self.config)

	@route('/scoreDistribution', methods=['POST'])
	def score_distribution(self):
		"""
			Method to compute scoren distribution from reviews data
		"""
		date = request.get_json().get('date', None)
		
		try:
			# computing stats
			score_distribution, review_distribution = self.analyser.compute_score_distribution(date=date)

			# Convert plot to PNG image
			plot = Plot(self.config)
			figure_plot_SD = plot.score_distribution(score_distribution, review_distribution, date=date)
			image_plot_SD = io.BytesIO()
			FigureCanvas(figure_plot_SD).print_png(image_plot_SD)
			plot.refresh()
			
			return Response(image_plot_SD.getvalue(), mimetype='image/png')

		except FileNotFoundError:
			return f"File '{self.config['export_path']}' not found. Launch scraping process to create it", 500

	@route('/means', methods=['POST'])
	def means(self):
		"""
			Method to compute statistics from reviews data
		"""
		# Retrieve url parameters
		time_delta = int(request.get_json().get('timeDelta', 30))
		nb_ignore = int(request.get_json().get('ignore', 0))

		try:
			# computing stats
			means = {
				'Cumulative mean': self.analyser.compute_cumulative_mean(),
				'Rolling average (1 month)': self.analyser.compute_rolling_mean(time_delta, nb_ignore),
				'Rolling sum of reviews (1 month)': self.analyser.compute_rolling_sum(time_delta, nb_ignore)
			}

			# Convert plot to PNG image
			plot = Plot(self.config)
			figure_plot_res = plot.means(means)
			image_plot_res = io.BytesIO()
			FigureCanvas(figure_plot_res).print_png(image_plot_res)
			plot.refresh()
		
			return Response(image_plot_res.getvalue(), mimetype='image/png')
		except FileNotFoundError:
			return f"File '{self.config['export_path']}' not found. Launch scraping process to create it", 500
		
	@route('/stats', methods=['POST'])
	def overall_stats(self):
		"""
			Method to compute statistics from reviews data
		"""
		lang = str(request.get_json()['lang'])
		keywords = request.get_json()['keywords']
		
		try:
			# computing stats
			means, nb_reviews = self.analyser.compute_mean()
			review_with_mention, review_in_lang, review_with_mention_1star = self.analyser.compute_mention(lang=lang, keywords=keywords)
			stats = {
				'means': means,
				'nb_reviews': nb_reviews,
				'review_in_lang': len(review_in_lang),
				'review_with_mention': len(review_with_mention),
				'review_with_mention_1star': len(review_with_mention_1star)
			}
			
			# return stats
			return stats, 200

		except FileNotFoundError:
			return f"File '{self.config['export_path']}' not found. Launch scraping process to create it", 500