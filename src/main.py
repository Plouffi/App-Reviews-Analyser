from data_manager import DataManager, plot_fehpass_mention, plot_score_distribution
from scraper import Scraper
from datetime import date as dt
from cloud import Cloud
import sys
import json


def load_config():
	with open("./ressources/config.json") as f:
		config = json.load(f)
	return config


def save_last_import():
	with open("./ressources/copy.txt", "w") as file:
		file.write(dt.today().strftime('%d/%m/%Y'))


def get_reviews():
	"""
		Method to fecth reviews from the Playstore
	"""
	config = load_config()
	dm = DataManager(config)
	s = Scraper(config)
	reviews = s.get_reviews(config["feh_release_date"])
	dm.insert_reviews(reviews)
	dm.export()


def compute_data():
	"""
		Method to compute statistics from reviews data
	"""
	config = load_config()
	dm = DataManager(config)
	try:
		# load data review in export file (path in config)
		dm.load()

		# computing stats
		score_distribution, review_distribution = dm.compute_score_distribution()
		means = {
			"Cumulative mean": dm.compute_cumulative_mean(),
			"Rolling average (1month)": dm.compute_rolling_mean()
		}
		review_with_mention, review_in_en, review_with_mention_1star = dm.compute_fehpass_mention()

		# display stats
		plot_score_distribution(score_distribution, review_distribution)
		dm.plot_res(means)
		dm.plot_overall_stats()
		plot_fehpass_mention(review_with_mention, review_in_en, review_with_mention_1star)
	except FileNotFoundError:
		print(f"File '{config['export_path']}' not found. Launch scrapping process to create it")


def make_wordcloud():
	"""
		Method to generate a word cloud. Images are save in "ressources" directory.
	"""
	config = load_config()
	dm = DataManager(config)
	try:
		# load data in export file (path in config)
		dm.load()

		reviews_before_fp = dm.get_reviews_as_dict(language="en", period="before")
		reviews_after_fp = dm.get_reviews_as_dict(language="en", period="after")

		cloud = Cloud(alpha=10.)
		cloud.load_reviews(reviews_before_fp, reviews_after_fp)
		cloud.cloud()

	except FileNotFoundError:
		print(f"File '{config['export_path']}' not found. Please check provided path is a valid path.")


def main():
	process = sys.argv[1]
	if process == "get_reviews":
		get_reviews()
	elif process == "compute_data":
		compute_data()
	elif process == "make_wordcloud":
		make_wordcloud()
	else:
		print("No process provided")


if __name__ == "__main__":
	main()
