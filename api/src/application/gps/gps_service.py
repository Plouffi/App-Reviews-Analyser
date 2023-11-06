from datetime import datetime as dt

from src.application.scraper.scraper_service import ScraperService
from src.domain.repository.reviews_repository import IReviewsRepository
from src.domain.repository.gps_app_repository import IGPSAppRepository
from src.domain.model.gps_app import GPSApp

class GPSService:

	scraper: ScraperService
	reviews_repo: IReviewsRepository
	gps_app_repo: IGPSAppRepository

	def __init__(self, config, reviews_repo: IReviewsRepository, gps_app_repo: IGPSAppRepository) -> None:
		self.scraper = ScraperService(config=config)
		self.reviews_repo = reviews_repo
		self.gps_app_repo = gps_app_repo

	def get_app(self, app_id: str) -> GPSApp:
		return self.gps_app_repo.get(app_id)

	def get_reviews(self,  start_date: dt, end_date: dt, language: str = "en", score: int = -1):
		mask_language = self.reviews_repo.get_series("language") == language if language in self.config["languages"] else "en"
		mask_start_period = start_date <= self.reviews_repo.get_index()
		mask_end_period = self.reviews_repo.get_index() < end_date
		mask_score = self.reviews_repo.get_series("score") == score if 0 < score <= 5 else self.reviews_repo.get_series("score").isin([1, 2, 3, 4, 5])
		return self.reviews_repo.get_reviews(mask_language & mask_start_period & mask_end_period & mask_score)

	def save_app(self, app_id: str):
		app = self.scraper.app_detail(app_id)
		self.gps_app_repo.insert(app)

	def save_reviews(self, app_id):
		app = self.get_app(app_id=app_id)
		reviews = self.scraper.get_reviews(app.released)
		self.reviews_repo.insert_reviews(reviews)
