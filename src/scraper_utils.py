import json
from datetime import datetime as dt
from typing import Union
from google_play_scraper.constants.google_play import Sort
from urllib.error import HTTPError
from urllib.request import urlopen, Request
from google_play_scraper.constants.regex import Regex
from google_play_scraper.constants.url import URLFormats
from google_play_scraper.exceptions import NotFoundError, ExtraHTTPError


def _urlopen(obj):
	try:
		resp = urlopen(obj)
	except HTTPError as e:
		if e.code == 404:
			raise NotFoundError("App not found(404).")
		else:
			raise ExtraHTTPError(
				"App not found. Status code {} returned.".format(e.code)
			)
	return resp.read().decode("UTF-8")


def _post(url: str, data: Union[str, bytes], headers: dict) -> str:
	return _urlopen(Request(url, data=data, headers=headers))


def reviews(
		app_id: str,
		lang: str = "en",
		sort: Sort = Sort.NEWEST,
		date: dt = dt.strptime('2017-02-02 1:00AM', '%Y-%m-%d %I:%M%p'),
		count: int = 1000000
) -> list:
	pagination_token = None

	def _fetch_review_items():
		nonlocal pagination_token

		if pagination_token is None:
			payload = (
				f"f.req=%5B%5B%5B%22UsvDTd%22%2C%22%5Bnull%2Cnull%2C%5B2%2C{sort}%2C%5B{_count}"
				f"%2Cnull%2Cnull%5D%2Cnull%2C%5B%5D%5D%2C%5B%5C%22{app_id}"
				f"%5C%22%2C7%5D%5D%22%2Cnull%2C%22generic%22%5D%5D%5D".encode()
			)
		else:
			payload = (
				f"f.req=%5B%5B%5B%22UsvDTd%22%2C%22%5Bnull%2Cnull%2C%5B2%2C{sort}%2C%5B{_count}"
				f"%2Cnull%2C%5C%22{pagination_token}%5C%22%5D%2Cnull%2C%5B%5D%5D%2C%5B%5C%22{app_id}"
				f"%5C%22%2C7%5D%5D%22%2Cnull%2C%22generic%22%5D%5D%5D".encode()
			)

		dom = _post(url, payload, {"content-type": "application/x-www-form-urlencoded"})
		reg = Regex.REVIEWS.findall(dom)
		match = json.loads(reg[0])
		try:
			pagination_token = json.loads(match[0][2])[-1][-1]
		except TypeError:
			return []
		return json.loads(match[0][2])[0]

	url = URLFormats.Reviews.build_url(lang=lang, country="US")

	if count < 200:
		_count = count
	else:
		_count = 199
	date_limit = dt.strptime('2017-02-02 1:00AM', '%Y-%m-%d %I:%M%p')
	if date < date_limit:
		date = date_limit
	result = []

	while True:
		review_items = _fetch_review_items()

		if len(review_items) == 0:
			break

		for review in review_items:
			try:
				user_name = review[1][0]
			except IndexError:
				user_name = None
			try:
				user_image = review[1][1][3][2]
			except IndexError:
				user_image = None
			try:
				content = review[4]
			except IndexError:
				content = None
			try:
				score = review[2]
			except IndexError:
				score = None
			try:
				thumbs_up_count = review[6]
			except IndexError:
				thumbs_up_count = None
			try:
				review_created_version = review[10]
			except IndexError:
				review_created_version = None
			try:
				at = dt.fromtimestamp(review[5][0])
			except IndexError:
				at = None

			result.append(
				{
					"userName": user_name,
					"userImage": user_image,
					"content": content,
					"score": score,
					"thumbsUpCount": thumbs_up_count,
					"reviewCreatedVersion": review_created_version,
					"at": at,
				}
			)

			if len(result) >= count or at < date:
				break
		else:
			continue
		break

	return result
