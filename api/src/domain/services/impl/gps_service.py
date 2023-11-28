from typing import List, Dict
from datetime import datetime as dt

from src.domain.services.i_gps_service import IGPSService
from src.domain.services.impl.scraper_service import ScraperService
from src.domain.repository.reviews_repository import IReviewsRepository
from src.domain.repository.gps_app_repository import IGPSAppRepository
from src.domain.model.gps_app import GPSApp, ExportStatus
from src.domain.model.review import Review


class GPSService(IGPSService):

	config: Dict
	scraper_service: ScraperService
	reviews_repo: IReviewsRepository
	gps_app_repo: IGPSAppRepository

	def __init__(self, config: Dict, scraper_service: ScraperService, reviews_repo: IReviewsRepository, gps_app_repo: IGPSAppRepository) -> None:
		self.config = config
		self.scraper_service = scraper_service
		self.reviews_repo = reviews_repo
		self.gps_app_repo = gps_app_repo

	def get_app(self, app_id: str) -> GPSApp:
		return self.gps_app_repo.get(app_id)

	def get_reviews(self, app_id:str, start_date: dt, end_date: dt, language: str = "en", score: int = -1) -> List[Review]:
		app = GPSApp(self.gps_app_repo.get(app_id))
		if app is not None:
			df = self.reviews_repo.get_df(app.exportPath)
			mask_language = self.reviews_repo.get_series(df, "language") == language if language in self.config['languages'] else "en"
			mask_start_period = start_date <= self.reviews_repo.get_index(df)
			mask_end_period = self.reviews_repo.get_index(df) < end_date
			mask_score = self.reviews_repo.get_series(df, "score") == score if 0 < score <= 5 else self.reviews_repo.get_series(df, "score").isin([1, 2, 3, 4, 5])
			return self.reviews_repo.get(df, mask_language & mask_start_period & mask_end_period & mask_score)
		else: 
			return []

	def save_app(self, app_id: str):
		app = self.scraper_service.app_detail(app_id)
		self.gps_app_repo.insert(app)
		self.gps_app_repo.commit()

	def save_reviews(self, app_id):
		app = self.get_app(app_id=app_id)
		if (app.exportStatus is ExportStatus.NO_EXPORT):
			try :
				self.change_export_status(app_id, ExportStatus.EXPORTING)
				reviews = self.scraper_service.get_reviews(app.released)
				export_path = self.get_export_path(app.id)
				self.reviews_repo.insert(reviews, export_path)
				update = [("exportPath", export_path), ("exportDate", dt.now().strftime("%d/%m/%Y"))]
				self.gps_app_repo.update(app_id, update)
				self.change_export_status(app_id, ExportStatus.EXPORTED)
			except:
				# TODO throw error
				self.gps_app_repo.rollback()
		else:
			# TODO renvoyer un message pour prévenir du status
			pass

	def change_export_status(self, app_id: str, new_status: ExportStatus) -> None:
		try:
			update = ("exportStatus", new_status)
			self.gps_app_repo.update(app_id, update)
			self.gps_app_repo.commit()
		except:
			self.gps_app_repo.rollback()
			# TODO: throw error

	def get_export_path(self, app_id: str) -> str:
		return f"{self.config['exportPath']}/{app_id}_export.csv"