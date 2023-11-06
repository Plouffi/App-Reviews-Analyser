import sqlite3
from sqlite3 import Connection, Cursor
from abc import ABC, abstractmethod

class SQLiteRepository(ABC):
	
	config: any
	connection: Connection
	cursor: Cursor

	def __init__(self, config, schema: str):
		self.config = config
		self.connection = sqlite3.connect(self.config["database"][schema]["path"])
		self.cursor = self.connection.cursor()

	def sqlite_commit(self): 
		self.connection.commit()

	def sqlite_rollback(self): 
		self.connection.rollback()