from data_manager import DataManager
from scraper import Scraper
from datetime import date as dt
from cloud import Cloud
from flask import Flask, request, Response, render_template
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import json

app = Flask(__name__)

def load_config():
	with open("./ressources/config.json") as f:
		config = json.load(f)
	return config

def save_last_import():
	with open("./ressources/copy.txt", "w") as file:
		file.write(dt.today().strftime('%d/%m/%Y'))

@app.route('/getReviews')
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
	return "OK", 200

@app.route('/compute/scoreDistribution', methods=['GET'])
def compute_score_distribution():
	"""
		Method to compute scoren distribution from reviews data
	"""
	date = request.args.get('date')
	config = load_config()
	dm = DataManager(config)
	try:
		# load data review in export file (path in config)
		dm.load()

		# computing stats
		score_distribution, review_distribution = dm.compute_score_distribution(date=date)

		# Convert plot to PNG image
		figure_plot_SD = dm.plot_score_distribution(score_distribution, review_distribution, date=date)
		image_plot_SD = io.BytesIO()
		FigureCanvas(figure_plot_SD).print_png(image_plot_SD)
		dm.plot_refresh()
		
		return Response(image_plot_SD.getvalue(), mimetype='image/png')

	except FileNotFoundError:
		return f"File '{config['export_path']}' not found. Launch scrapping process to create it", 500

@app.route('/compute/means', methods=['GET'])
def compute_means():
	"""
		Method to compute statistics from reviews data
	"""
	# Retrieve url parameters
	time_delta = int(request.args.get('timeDelta')) if request.args.get('timeDelta') is not None else 30
	nb_ignore = int(request.args.get('ignore')) if request.args.get('ignore') is not None else 0

	config = load_config()
	dm = DataManager(config)
	try:
		# load data review in export file (path in config)
		dm.load()

		# computing stats
		means = {
			"Cumulative mean": dm.compute_cumulative_mean(),
			"Rolling average (1 month)": dm.compute_rolling_mean(time_delta, nb_ignore),
			"Rolling sum of reviews (1 month)": dm.compute_rolling_sum(time_delta, nb_ignore)
		}

		# Convert plot to PNG image
		figure_plot_res = dm.plot_res(means)
		image_plot_res = io.BytesIO()
		FigureCanvas(figure_plot_res).print_png(image_plot_res)
		dm.plot_refresh()
	
		return Response(image_plot_res.getvalue(), mimetype='image/png')
	except FileNotFoundError:
		return f"File '{config['export_path']}' not found. Launch scrapping process to create it", 500
	
@app.route('/compute/stats', methods=['GET'])
def compute_overall_stats():
	"""
		Method to compute statistics from reviews data
	"""
	config = load_config()
	dm = DataManager(config)
	try:
		# load data review in export file (path in config)
		dm.load()

		# computing stats
		means, nb_reviews = dm.compute_mean()
		review_with_mention, review_in_lang, review_with_mention_1star = dm.compute_fehpass_mention()
		stats = {
					"means": means,
					"nb_reviews": nb_reviews,
					"review_in_lang": len(review_in_lang),
					"review_with_mention": len(review_with_mention),
					"review_with_mention_1star": len(review_with_mention_1star)
				}
		
		# return stats
		return stats, 200

	except FileNotFoundError:
		return f"File '{config['export_path']}' not found. Launch scrapping process to create it", 500

@app.route('/wordcloud', methods=['GET'])
def make_wordcloud():
	"""
		Method to generate a word cloud. Images are save in "ressources" directory.
	"""
	alpha = float(request.args.get('alpha')) if request.args.get('alpha') is not None else 10
	n = int(request.args.get('n')) if request.args.get('n') is not None else 2
	start_date_1 = request.args.get('start1')
	start_date_2 = request.args.get('start2')
	end_date_1 = request.args.get('end1')
	end_date_2 = request.args.get('end2')
	lang = str(request.args.get('lang'))
	score = int(request.args.get('score')) if request.args.get('score') is not None else -1
	config = load_config()
	dm = DataManager(config)
	try:
		# load data in export file (path in config)
		dm.load()

		reviews_before_fp = dm.get_reviews_as_dict(start_date=start_date_1, end_date=end_date_1, language=lang, score=score)
		reviews_after_fp = dm.get_reviews_as_dict(start_date=start_date_2, end_date=end_date_2, language=lang, score=score)
		cloud = Cloud(alpha=alpha, n=n)
		cloud.load_reviews(reviews_before_fp, reviews_after_fp)
		cloud.cloud()
		return render_template('wordcloud.html')

	except FileNotFoundError:
		print(f"File '{config['export_path']}' not found. Please check provided path is a valid path.")


if __name__ == "__main__":
	#get_reviews()
	app.run()
