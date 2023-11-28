from typing import Tuple, Dict

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
			gps_app.score, 
			gps_app.realInstalls, 
			gps_app.released,
			gps_app.exportPath, 
			gps_app.exportDate, 
			gps_app.exportPath
		]) + "'"
		super().cursor.execute(f"INSERT INTO {self.table} VALUES ({values})")

	def get(self, app_id: str):
		res = super().cursor.execute(f"SELECT * FROM {self.table} WHERE appId ='{app_id}'")
		return res.fetchone()

	def update(self, app_id: str, *fieldsValue: Tuple[str, str]):
		update = ", ".join([f"{field}='{value}'" for field, value in fieldsValue])
		super().cursor.execute(f"UPDATE {self.table} SET {update} WHERE appId ='{app_id}'")

	def commit(self): 
		super().sqlite_commit()

	def rollback(self): 
		super().sqlite_rollback()