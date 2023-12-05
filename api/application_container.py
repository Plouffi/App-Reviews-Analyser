import os, json
from dependency_injector import containers, providers

from src.domain.services.impl.gps_service import GPSService
from src.domain.services.impl.scraper_service import ScraperService
from src.domain.services.impl.analyser_service import AnalyserService
from src.domain.services.impl.plot_service import PlotService
from src.domain.services.impl.cloud_service import CloudService
from src.domain.services.impl.make_image import MakeImageService
from src.infrastructure.dataframe.impl.reviews_df import ReviewsDF
from src.infrastructure.sqlite.impl.gps_app_sqlite_repository import GPSAppSQLite

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class ApplicationContainer(containers.DeclarativeContainer):
	"""Application container."""

	config = providers.Configuration(yaml_files=["./resources/config.yaml"])
	
	wiring_config = containers.WiringConfiguration(packages=["src"])

	reviews_df_repo = providers.Factory(
		ReviewsDF,
		config=config,
		root_dir=ROOT_DIR
	)
	gps_app_sqlite_repo = providers.Factory(
		GPSAppSQLite,
		config=config,
		root_dir=ROOT_DIR
	)

	# Services
	scraper_service = providers.Factory(
		ScraperService,
		config=config
	)
	gps_service =  providers.Factory(
		GPSService,
		config=config,
		scraper_service=scraper_service,
		reviews_repo=reviews_df_repo,
		gps_app_repo=gps_app_sqlite_repo
	)
	analyser_service = providers.Factory(
		AnalyserService,
		reviews_repo=reviews_df_repo,
		gps_app_repo=gps_app_sqlite_repo
	)
	plot_service = providers.Factory(
		PlotService,
		config=config
	)
	cloud_service = providers.Factory(
		CloudService
	)
	make_service = providers.Factory(
		MakeImageService,
		config=config
	)