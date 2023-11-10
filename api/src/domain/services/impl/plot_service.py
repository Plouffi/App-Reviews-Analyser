from typing import List, Dict
from datetime import datetime as dt
import numpy as np
from pandas import Series
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import Figure

from src.domain.services.i_plot_service import IPlotService

matplotlib.use('agg') # Enable plot on a web app context
class PlotService(IPlotService):
	"""A class to generate plot from app data.
		----------
		Attributes
		config (Dict): Program's configuration.
	"""
	config: Dict
	
	def __init__(self, config: Dict):
		"""
			Parameters
			----------
			config (Dict): Program's configuration.
		"""
		self.config = config

	def means(self, cumulative_mean: Series, rolling_mean: Series, rolling_sum: Series) -> Figure:
		stats = { 
			'Cumulative mean': cumulative_mean,
			'Rolling average (1 month)': rolling_mean,
			'Rolling sum of reviews (1 month)': rolling_sum
		}
		# plt.axvline(x=self.feh_pass_date, ls="--", color="#e55039", linewidth=1, label="Feh Pass announcement")

		fig, ax_score = plt.subplots()
		#ax_score = axes.Axes()
		ax_score.set_ylabel('Score')
		ax_score.set_ylim(1,5)

		# plot data
		for ((k, v), color, i) in zip(stats.items(), ["#009432", "#9980FA", "#E55039"], range(3)):
			if i < 2:
				ax_score.plot(v, label=k, color=color)
			else:
				# Last set of data has a different scale so we make an other y axis
				ax_reviews = ax_score.twinx()
				ax_reviews.set_ylabel("Number of review", labelpad=15)
				reviews_max = v.max()
				ax_reviews.set_ylim(0, reviews_max * 11/10) 
				ax_reviews.plot(v, label=k, color=color)

		# format date labels
		ax = plt.gca()
		formatter = mdates.DateFormatter("%b %Y")
		ax.xaxis.set_major_formatter(formatter)

		#plt.xlim(dt.strptime(self.config["feh_release_date"], "%Y-%m-%d %I:%M%p"))
		plt.title("Cumulative mean, rolling average and cumulative number \n of reviews on FEH score from playstore")

		# display
		return plt.gcf()

	def score_distribution(self, reviews_distribution: List[List[float]], nb_reviews: List[int], date: dt) -> Figure:
		# remove the "after" data if date is None
		if date is None:
			reviews_distribution.pop()
		# data to plot
		data = np.array(reviews_distribution)
		data = data.T

		# plot grid
		plt.rc("grid", ls="-", color="#ced6e0")
		plt.grid(axis="y", zorder=0)

		# plot data
		index = np.arange(2 if date is not None else 1)
		bar_width = 0.1
		colors = ["#78e08f", "#9fc552", "#bfa525", "#d87e1d", "#e55039"]
		labels = ["5 stars", "4 stars", "3 stars", "2 stars", "1 star"]
		for i, color, label in zip(range(0, 5), colors, labels):
			plt.bar(index + i * bar_width, data[i], bar_width, color=color, label=label, zorder=3)

		# add labels and legends
		plt.ylabel("% of reviews")
		plt.ylim(0, 100)
		title = " before and after " + date if date is not None else ""
		plt.title("% of reviews by score" + title)
		if date is not None:
			tickBefore = "%s reviews" % '{:,}'.format(nb_reviews[0]).replace(',', ' ') + "\n before " + date
			tickAfter = "%s reviews" % '{:,}'.format(nb_reviews[1]).replace(',', ' ') + "\n after " + date
			plt.xticks(index + 2 * bar_width, (tickBefore, tickAfter))
		else:
			plt.xticks(index + 2 * bar_width, ["%s reviews" % '{:,}'.format(nb_reviews[0]).replace(',', ' ')])

		plt.legend()
		return plt.gcf()

	def refresh(self) -> None:
		plt.clf()
		plt.cla()