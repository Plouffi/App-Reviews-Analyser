from typing import Dict, Tuple, List
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime as dt
import matplotlib

matplotlib.use('agg')

class DataManager:
	"""
	A class to handle and compute statistics about feh pass.
	...
		Attributes
		----------
		config : Dict
			Program's configuration.
		df : Dataframe
		feh_pass_date : dt
			Date of the announcement of FEH pass
	"""
	def __init__(self, config):
		"""
			Parameters
			----------
			config : Dict
				Program's configuration.

		"""
		columns = ["userName", "content", "score", "thumbsUpCount", "reviewCreatedVersion", "at", "language"]
		self.df = pd.DataFrame(columns=columns)
		self.config = config
		self.feh_pass_date = dt.strptime(self.config["feh_pass_date"], "%Y-%m-%d %I:%M%p")

	def insert_reviews(self, reviews):
		"""
		Method to store data review in a Dataframe
			Parameters
			----------
			reviews : Lis(Dict)
				Array of dictionnary containing data review

		"""
		series_reviews = []
		for review in reviews:
			series_reviews.append(pd.Series(review.items(), index=self.df.columns))
		self.df = self.df._append(reviews, ignore_index=True)

	def get_reviews(self):
		"""
		Return the Dataframe
		"""
		return self.df

	def get_reviews_as_dict(self, language: str = "en", date: dt = None, period: str = "after", score: int = -1) -> Dict:
		"""
		Method to research reviews by passing parameters (language, date, period, score). Return them as a dictionnary
			Parameters
			----------
			language : str = "en"
				Research parameter: review's language. Set up to "en" if language doesn't exist in configuration file.
			date : datetime = None
				Research parameter: date where we start the research. Default date is set to feh pass announcement.
			period : str = "after"
				Research parameter: "direction" of the date research. "before" --> all reviews before the date
				/ "after" same logic
			score : int = -1
				Research parameter: review's score. Can be in [1...5] or anything else to have all range

			Returns
			-------
				Dict
					A dictionnary of reviews
		"""
		date = self.feh_pass_date if date is None else date
		mask_language = self.df["language"] == language if language in self.config["languages"] else "en"
		mask_period = self.df.index < date if period == "before" else self.df.index >= date
		mask_score = self.df["score"] == score if 0 < score <= 5 else self.df["score"].isin([1, 2, 3, 4, 5])
		mask = mask_language & mask_period & mask_score

		return self.df.loc[mask].to_dict('records')

	def load(self):
		"""
		Method to load reviews from csv file. Set up the dataframe's index on "at" column (publication date)
		"""
		self.df = pd.read_csv(self.config["export_path"])
		# set up the index on publishing date and sort the dataframe
		self.df["at"] = pd.to_datetime(self.df["at"])
		self.df = self.df.set_index("at")
		self.df = self.df.sort_values("at", ascending=True)

	def export(self):
		"""
		Method to export reviews in csv.
		"""
		self.df.to_csv(self.config["export_path"], index=False)
		print(f"Reviews exported in '{self.config['export_path']}'. Total: {len(self.df.index)} records.")

	def get_num_reviews(self) -> int:
		"""
		Method to load reviews from csv file. Set up the dataframe's index on "at" column (publication date)
			Returns
			-------
				int
				The number of reviews
		"""
		dfpy = self.df["score"].to_numpy()
		return len(dfpy)

	def compute_mean(self) -> Tuple[np.ndarray, int]:
		"""
		Method to compute mean of reviews' score.
			Returns
			-------
				Tuple[np.ndarray,int]
					The mean and the number of reviews
		"""
		dfpy = self.df["score"].to_numpy()
		return np.mean(dfpy), len(dfpy)

	def compute_rolling_mean(self) -> pd.Series:
		"""
		Method to compute rolling mean of reviews' score. The windows is set to 1 month because it's almost the
		frequency of FEH updates
			Returns
			-------
				pd.Series
		"""
		# iloc[1000:] remove an arbitrary amount of data in head to avoid irrelevant data while computing first values
		return self.df["score"].iloc[1000:].rolling("30D").mean()

	def compute_cumulative_mean(self) -> pd.Series:
		"""
		Method to compute cumulative mean of reviews' score.
			Returns
			-------
				pd.Series
		"""
		# iloc[1000:] remove an arbitrary amount of data in head to avoid irrelevant data while computing first values
		return self.df["score"].iloc[1000:].expanding().mean()

	def compute_score_distribution(self) -> Tuple[List[List[float]], List[int]]:
		"""
		Method to compute score distribution before and after FEH pass.
			Returns
			-------
			List(List(int))
				A 2-dimensionnal array representing score distribution before and after FEH pass.
				Shape should be (2, 5) 2--> before/after // 5--> score range
			List(int)
				An array stocking the number of reviews published before and after FEH pass
		"""
		def get_score_distribution(data):
			score_distribution = []
			for i in range(5, 0, -1):
				pourcent = len(data.loc[data["score"] == i]) / len(data) * 100
				score_distribution.append(pourcent)
			return score_distribution

		before_fp = self.df.loc[(self.df.index < self.feh_pass_date)]
		after_fp = self.df.loc[(self.df.index >= self.feh_pass_date)]

		return [get_score_distribution(before_fp), get_score_distribution(after_fp)], [len(before_fp), len(after_fp)]

	def compute_fehpass_mention(self) -> Tuple[pd.Series,  pd.Series, pd.Series]:
		"""
		Method to compute stats about FEH pass mentions in english reviews. Native detection, check if the content one
		of the keywords defined in the configuration file.
			Returns
			-------
			Tuple[pd.Series,  pd.Series, pd.Series]
		"""
		mask_language = self.df["language"] == "en"
		mask_period = self.df.index >= self.feh_pass_date
		mask_mention = self.df["content"].str.contains('|'.join(self.config["feh_pass_en_keywords"]))
		mask_score = self.df["score"] == 1
		mask = mask_language & mask_period
		mask_with_mention = mask & mask_mention
		mask_1star_with_mention = mask_with_mention & mask_score

		return self.df.loc[mask], self.df.loc[mask_with_mention], self.df.loc[mask_1star_with_mention]

	# plot methods

	def plot_res(self, stats):
		"""
		Method to plot the graph displaying curves of rolling average and cumulative mean.
		"""
		# plot grid
		plt.rc("grid", ls="--", color="#ced6e0")
		plt.grid()

		# plot feh pass announcement
		plt.axvline(x=self.feh_pass_date, ls="--", color="#e55039", linewidth=1, label="Feh Pass announcement")

		# plot data
		for ((k, v), color) in zip(stats.items(), ["#009432", "#9980FA"]):
			plt.plot(v, label=k, color=color)

		# format date labels
		ax = plt.gca()
		formatter = mdates.DateFormatter("%b %Y")
		ax.xaxis.set_major_formatter(formatter)
		plt.xticks(rotation=25, ha="right", rotation_mode="anchor")
		# set up limit
		plt.ylim(1, 5)
		plt.xlim(dt.strptime(self.config["feh_release_date"], "%Y-%m-%d %I:%M%p"))
		# add legends and label
		plt.legend(loc="best")
		plt.xlabel("Time")
		plt.ylabel("Score")
		plt.text(
			dt.strptime("2017-05-01 01:00AM", "%Y-%m-%d %I:%M%p"),
			2,
			"%s reviews" % '{:,}'.format(self.get_num_reviews()).replace(',', ' ')
		)
		plt.title("Cumulative mean and rolling average on FEH score from playstore")

		# display
		return plt.gcf()
	
	def plot_score_distribution(self, reviews_distribution, nb_reviews):
		"""
		Plot a bar chart showing reviews' score ditribution.
			Parameters
			----------
			reviews_distribution : List(List(float))
				A 2-dimensionnal array representing score distribution before and after FEH pass.
				Shape should be (2, 5) 2--> before/after // 5--> score range
			nb_reviews : List(int)
				An array stocking the number of reviews published before and after FEH pass
		"""
		# data to plot
		data = np.array(reviews_distribution)
		data = data.T

		# plot grid
		plt.rc("grid", ls="-", color="#ced6e0")
		plt.grid(axis="y", zorder=0)

		# plot data
		index = np.arange(2)
		bar_width = 0.1
		colors = ["#78e08f", "#9fc552", "#bfa525", "#d87e1d", "#e55039"]
		labels = ["5 stars", "4 stars", "3 stars", "2 stars", "1 star"]
		for i, color, label in zip(range(0, 5), colors, labels):
			plt.bar(index + i * bar_width, data[i], bar_width, color=color, label=label, zorder=3)

		# add labels and legends
		plt.ylabel("% of reviews")
		plt.ylim(0, 100)
		plt.title("% of reviews by score before and after FEH Pass announcement")
		plt.xticks(index + 2 * bar_width, ("Before FEH Pass", "After FEH Pass"))
		plt.text(0, 80, "%s reviews" % '{:,}'.format(nb_reviews[0]).replace(',', ' '))
		plt.text(1, 60, "%s reviews" % '{:,}'.format(nb_reviews[1]).replace(',', ' '))
		plt.legend()
		return plt.gcf()
		
	def plot_refresh(self):
		"""
			Refresh the current plot
		"""
		plt.clf()
		plt.cla()
