import os
from dependency_injector import containers, providers
from dependency_injector.ext import flask
from flask import Flask

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

	app = flask.Application(Flask, __name__)

	config = providers.Configuration(yaml_files=["./resources/config.yaml"])

	# Repositories
	reviews_df_repo = providers.Factory(
		ReviewsDF,
		columns=config.dataframe.reviews
	)
	gps_app_sqlite_repo = providers.Factory(
		GPSAppSQLite,
		path=f"{ROOT_DIR}/{config.database.ara.path}"
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
		config=config,
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
		path_to_font=config.pathToFont
	)