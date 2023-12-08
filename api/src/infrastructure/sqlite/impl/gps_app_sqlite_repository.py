from typing import Tuple, Dict, List
from datetime import datetime

from src.infrastructure.sqlite.sqlite_repository import SQLiteRepository
from src.domain.repository.gps_app_repository import IGPSAppRepository
from src.domain.model.gps_app import GPSApp

class GPSAppSQLite(SQLiteRepository, IGPSAppRepository):
  
	table: str

	def __init__(self, config: Dict, root_dir: str):
		super().__init__(f"{root_dir}{config['database']['ara']['path']}")
		self.table = "GPS_APP"

	def insert(self, gps_app: GPSApp):
		values = "'" + "','".join([
			gps_app.id,
			gps_app.title,
			gps_app.developer,
			gps_app.version,
			gps_app.icon,
			gps_app.headerImage, 
			str(gps_app.score), 
			str(gps_app.realInstalls), 
			str(gps_app.released),
			gps_app.exportPath, 
			gps_app.exportDate if gps_app.exportDate is not None else 'NULL', 
			str(gps_app.exportStatus)
		]) + "'"
		self.cursor.execute(f"INSERT INTO {self.table} VALUES ({values})")

	def get(self, app_id: str) -> GPSApp:
		res = self.cursor.execute(f"SELECT * FROM {self.table} WHERE appId ='{app_id}'")
		row = res.fetchone()
		if row is not None:
			fields = [column[0] for column in self.cursor.description]
			app = {key: value for key, value in zip(fields, row)}
			app['released'] = datetime.strptime(app['released'], '%Y-%m-%d %H:%M:%S').strftime('%b %d, %Y %H:%M')
			return GPSApp(app)
		else:
			# throw exception
			return None

	def list(self) -> List[GPSApp]:
		res = self.cursor.execute(f"SELECT * FROM {self.table} WHERE exportStatus='2'")
		rows = res.fetchall()
		if rows:
			apps = []
			for row in rows:
				fields = [column[0] for column in self.cursor.description]
				app = {key: value for key, value in zip(fields, row)}
				app['released'] = datetime.strptime(app['released'], '%Y-%m-%d %H:%M:%S').strftime('%b %d, %Y %H:%M')
				apps.append(GPSApp(app))
			return apps
		else:
			# throw exception
			return rows

	def update(self, app_id: str, *fieldsValue: Tuple[str, str]):
		update = ", ".join([f"{field}='{value}'" for field, value in fieldsValue])
		self.cursor.execute(f"UPDATE {self.table} SET {update} WHERE appId ='{app_id}'")

	def commit(self): 
		self.sqlite_commit()

	def rollback(self): 
		self.sqlite_rollback()