
from flask_cors import CORS
from flask import Flask
from dependency_injector.ext import flask


from application_container import ApplicationContainer


def create_app():
	"""
		Configure the app and views
	"""
	container = ApplicationContainer()
	app = flask.Application(Flask, __name__)()
	CORS(app, resources={r"/api/*": {"origins": "*"}})

	base_api_url = "/api/v1.0"
	register_application(app, base_api_url)

	return app


def register_application(app, base_api_url: str):
	"""
		Setup the base routes for various features.
	"""
	from src.application.gps_app_controller import GPSAppController
	from src.application.analyser_controller import AnalyserController
	from src.application.wordcloud_controller import WordcloudController

	GPSAppController.register(app, route_base=f"{base_api_url}/gpsApp")
	AnalyserController.register(app, route_base=f"{base_api_url}/analyser")
	WordcloudController.register(app, route_base=f"{base_api_url}/wordcloud")

if __name__ == '__main__':
	create_app().run()