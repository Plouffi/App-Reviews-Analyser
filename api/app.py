from src.Cloud.cloud import Cloud
from src.DataManager.data_manager import DataManager
from src.Plot.plot import Plot
from src.Scraper.scraper import Scraper
import src.Image.make_image as make_image

from flask import Flask, jsonify, request, Response, render_template
from hashlib import sha256
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import json
import os

app = Flask(__name__)

def load_config():
	with open('./ressources/config.json', errors='replace') as f:
		config = json.load(f)
	return config

# def find_file(hash: str) -> str:
# 	if hash is None:
# 		return ''
# 	else:
# 		filename = ''
# 		for fn in os.listdir('./tmp'):
# 			if sha256(fn).hexdigest() == hash:
# 				filename = fn
# 		return filename



# @app.route('/uploadData', methods=['POST'])
# def save_last_import():
# 	with open('./ressources/copy.txt', 'w') as file:
# 		file.write(dt.today().strftime('%d/%m/%Y'))
# 	"""
# 		Method to upload a csv file to the server for later computation
# 		Returns
# 			-------
# 				str
# 				The hashed filename
# 	"""
# 	# Retrieve file and save it
# 	f = request.files['fileData']
# 	f.filename = f.filename + '_' + str(dt.now())
# 	f.save('./tmp/' + f.filename)

# 	# We send the hashed filename to the client to be able to find the file later
# 	return sha256(f.filename).hexdigest()

@app.route('/searchApp')
def search_apps():
	"""
		Method to search app on playstore
	"""
	search = request.args.get('search')
	config = load_config()
	try:
		s = Scraper(config)
		return config['mockSearch']
		#return s.search_app(search)

	except FileNotFoundError:
		return f"File '{config['export_path']}' not found. Launch scrapping process to create it", 500
	
@app.route('/appDetail')
def app_detail():
	"""
		Method to get app detail on playstore
	"""
	id = request.args.get('id')
	config = load_config()
	try:
		s = Scraper(config)
		return config['mockDetail']
		#return s.app_detail(id)

	except FileNotFoundError:
		return f"File '{config['export_path']}' not found. Launch scrapping process to create it", 500

@app.route('/getReviews')
def get_reviews():
	"""
		Method to fecth reviews from the Playstore
	"""
	config = load_config()
	dm = DataManager(config)
	s = Scraper(config)
	reviews = s.get_reviews(config['feh_release_date'])

	return 'OK', 200

@app.route('/compute/scoreDistribution', methods=['POST'])
def compute_score_distribution():
	"""
		Method to compute scoren distribution from reviews data
	"""
	date = request.get_json().get('date', None)
	config = load_config()
	dm = DataManager(config)
	try:
		# load data review in export file (path in config)
		dm.load()

		# computing stats
		score_distribution, review_distribution = dm.compute_score_distribution(date=date)

		# Convert plot to PNG image
		plot = Plot(config)
		figure_plot_SD = plot.score_distribution(score_distribution, review_distribution, date=date)
		image_plot_SD = io.BytesIO()
		FigureCanvas(figure_plot_SD).print_png(image_plot_SD)
		plot.refresh()
		
		return Response(image_plot_SD.getvalue(), mimetype='image/png')

	except FileNotFoundError:
		return f"File '{config['export_path']}' not found. Launch scrapping process to create it", 500

@app.route('/compute/means', methods=['POST'])
def compute_means():
	"""
		Method to compute statistics from reviews data
	"""
	# Retrieve url parameters
	time_delta = int(request.get_json().get('timeDelta', 30))
	nb_ignore = int(request.get_json().get('ignore', 0))

	config = load_config()
	dm = DataManager(config)
	try:
		# load data review in export file (path in config)
		dm.load()

		# computing stats
		means = {
			'Cumulative mean': dm.compute_cumulative_mean(),
			'Rolling average (1 month)': dm.compute_rolling_mean(time_delta, nb_ignore),
			'Rolling sum of reviews (1 month)': dm.compute_rolling_sum(time_delta, nb_ignore)
		}

		# Convert plot to PNG image
		plot = Plot(config)
		figure_plot_res = plot.means(means)
		image_plot_res = io.BytesIO()
		FigureCanvas(figure_plot_res).print_png(image_plot_res)
		plot.refresh()
	
		return Response(image_plot_res.getvalue(), mimetype='image/png')
	except FileNotFoundError:
		return f"File '{config['export_path']}' not found. Launch scrapping process to create it", 500
	
@app.route('/compute/stats', methods=['POST'])
def compute_overall_stats():
	"""
		Method to compute statistics from reviews data
	"""
	lang = str(request.get_json()['lang'])
	keywords = request.get_json()['keywords']

	config = load_config()
	dm = DataManager(config)
	try:
		# load data review in export file (path in config)
		dm.load()

		# computing stats
		means, nb_reviews = dm.compute_mean()
		review_with_mention, review_in_lang, review_with_mention_1star = dm.compute_mention(lang=lang, keywords=keywords)
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
		return f"File '{config['export_path']}' not found. Launch scrapping process to create it", 500

@app.route('/wordcloud/computeWords', methods=['POST'])
def compute_words():
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
	config = load_config()
	dm = DataManager(config)
	try:
		# load data in export file (path in config)
		dm.load()

		reviews_before_fp = dm.get_reviews_as_dict(start_date=start_date_1, end_date=end_date_1, language=lang, score=score)
		reviews_after_fp = dm.get_reviews_as_dict(start_date=start_date_2, end_date=end_date_2, language=lang, score=score)
		cloud = Cloud(alpha=alpha, n=n)
		cloud.load_reviews(reviews_before_fp, reviews_after_fp)
		return cloud.get_words()

	except FileNotFoundError:
		print(f"File '{config['export_path']}' not found. Please check provided path is a valid path.")

@app.route('/wordcloud/generateImage', methods=['POST'])
def generate_wordcloud():
	"""
		Method to generate a word cloud from an array of words and frequencies.
	"""
	words = request.get_json()['words']
	wordcloud = make_image.simple_image(words)

	# Convert plot to PNG image
	image = io.BytesIO()
	wordcloud.save(image, format='PNG')

	return Response(image.getvalue(), mimetype='image/png')


if __name__ == '__main__':
	#get_reviews()
	app.run()
