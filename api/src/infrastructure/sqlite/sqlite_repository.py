import sqlite3
from sqlite3 import Connection, Cursor
from abc import ABC, abstractmethod

class SQLiteRepository(ABC):
	
	connection: Connection
	cursor: Cursor

	def __init__(self, path: str):
		print(path)
		self.connection = sqlite3.connect(path, check_same_thread=False)
		self.cursor = self.connection.cursor()

	def sqlite_commit(self): 
		self.connection.commit()

	def sqlite_rollback(self): 
		self.connection.rollback()