import json
from typing import Any, Dict, List, Tuple
from datetime import datetime
from time import sleep
from urllib.parse import quote

from google_play_scraper import Sort
from google_play_scraper.constants.element import ElementSpec, ElementSpecs
from google_play_scraper.constants.regex import Regex
from google_play_scraper.constants.request import Formats
from google_play_scraper.exceptions import NotFoundError
from google_play_scraper.utils.request import get
from google_play_scraper.utils.data_processors import unescape_text
from google_play_scraper.features.reviews import MAX_COUNT_EACH_FETCH, _ContinuationToken, _fetch_review_items

"""
	I override search and reviews scraping function for 2 things
		- I don't want to fetch reviews older than the targeted app released date
		- I want to fetch the main app if one is found while performing search 
"""

# Main app result scrap mapping
MainAppResult = {
	"appId": ElementSpec(None, [16, 11, 0, 0]),
	"icon": ElementSpec(None, [16, 2, 95, 0, 3, 2]),
	"title": ElementSpec(None, [16, 2, 0, 0]),
	"score": ElementSpec(None, [16, 2, 51, 0, 1]),
	"price": ElementSpec(
		None, [17, 0, 2, 0, 1, 0, 0], lambda price: (price / 1000000) or 0
	),
	"free": ElementSpec(None, [17, 0, 2, 0, 1, 0, 0], lambda s: s == 0),
	"currency": ElementSpec(None, [17, 0, 2, 0, 1, 0, 1]),
	"description": ElementSpec(None, [16, 2, 73, 0, 1], unescape_text),
	"descriptionHTML": ElementSpec(None, [16, 2, 73, 0, 1]),
	"developer": ElementSpec(None, [16, 2, 68, 0]),
}

def search(
    query: str, n_hits: int = 30, lang: str = "en", country: str = "us"
) -> Dict[str, Any]:
	query = quote(query)
	url = Formats.Searchresults.build(query=query, lang=lang, country=country)
	try:
		dom = get(url)
	except NotFoundError:
		url = Formats.Searchresults.fallback_build(query=query, lang=lang)
		dom = get(url)

	matches = Regex.SCRIPT.findall(dom)

	dataset_main_app = {}
	dataset = {}

	for match in matches:
		key_match = Regex.KEY.findall(match)
		value_match = Regex.VALUE.findall(match)

		if key_match and value_match:
			key = key_match[0]
			value = json.loads(value_match[0])
			dataset[key] = value

	success_main_app = False
	success_more_result = False
	# different idx for different countries and languages
	for idx in range(len(dataset["ds:4"][0][1])):
		try:
			if not success_main_app and dataset["ds:4"][0][1][idx][23] is not None:
				dataset_main_app =  dataset["ds:4"][0][1][idx][23] # main app location
				success_main_app = True
		except Exception:
			pass
		try:
			dataset = dataset["ds:4"][0][1][idx][22][0]
			success_more_result = True
		except Exception:
			pass

	search_results = []

	if success_main_app:
		app = {}
		for k, spec in MainAppResult.items():
			content = spec.extract_content(dataset_main_app)
			app[k] = content
		search_results.append(app)

	if success_more_result:
		n_apps = min(len(dataset), n_hits)
		for app_idx in range(n_apps):
			app = {}
			for k, spec in ElementSpecs.Searchresult.items():
				content = spec.extract_content(dataset[app_idx])
				app[k] = content
			search_results.append(app)

	return search_results

def reviews(
	app_id: str,
	date: datetime,
	lang: str = "en",
	country: str = "us",
	sort: Sort = Sort.NEWEST,
	count: int = 100,
	filter_score_with: int = None,
	continuation_token: _ContinuationToken = None,
) -> Tuple[List[dict], _ContinuationToken]:
	if continuation_token is not None:
		token = continuation_token.token

		if token is None:
			return (
				[],
				continuation_token,
			)

		lang = continuation_token.lang
		country = continuation_token.country
		sort = continuation_token.sort
		count = continuation_token.count
		filter_score_with = continuation_token.filter_score_with
	else:
		token = None

	url = Formats.Reviews.build(lang=lang, country=country)

	_fetch_count = count

	result = []

	while True:
		if _fetch_count == 0:
			break

		if _fetch_count > MAX_COUNT_EACH_FETCH:
			_fetch_count = MAX_COUNT_EACH_FETCH

		try:
			review_items, token = _fetch_review_items(
			url, app_id, sort, _fetch_count, filter_score_with, token
			)
		except (TypeError, IndexError):
			token = None
			break

		for review in review_items:
			extracted_review = {
				k: spec.extract_content(review)
				for k, spec in ElementSpecs.Review.items()
			}
			# We don't want reviews publish before a certain date (mainly the app released date)
			if extracted_review['at'] < date:
				break
			
			result.append(extracted_review)

		_fetch_count = count - len(result)

		if isinstance(token, list):
			token = None
			break

	return (
		result,
		_ContinuationToken(token, lang, country, sort, count, filter_score_with),
	)

def reviews_all(app_id: str, date: datetime, sleep_milliseconds: int = 0, **kwargs) -> list:
	kwargs.pop("count", None)
	kwargs.pop("continuation_token", None)

	continuation_token = None

	result = []

	while True:
		_result, continuation_token = reviews(
			app_id,
			date,
			count=MAX_COUNT_EACH_FETCH,
			continuation_token=continuation_token,
			**kwargs
		)

		result += _result

		if continuation_token.token is None:
			break

		if sleep_milliseconds:
			sleep(sleep_milliseconds / 1000)

	return result