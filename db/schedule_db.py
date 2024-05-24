import sqlite3
from sqlite3 import Error

class ScheduleDB:

	def __init__(self):
		self.__connection = self.__connectDataBase()
		self.__cursor = self.__connection.cursor() if self.__connection else None

	def __del__(self):
		self.__connection.close()

	def __connectDataBase(self):
		try:
			connection = sqlite3.connect('schedule.db')
			return connection
		except Error:
			return None

	def createNewGroup(self, tableName):
		if self.__cursor:
			self.__cursor.execute("""CREATE TABLE IF NOT EXISTS {}(
				"id" INTEGER PRIMARY KEY AUTOINCREMENT,
				"date" DATETIME,
				"time_lesson"	TEXT,
				"subject_name"	TEXT,
				"description"	TEXT,
				"subgroup_number"	INTEGER,
				"teacher_name"	TEXT,
				"link_lesson"	TEXT)""".format(tableName))
			self.__connection.commit()

	def insertData(self, tableName, date, timeLesson, subjectName, description, subgroupNumber, teacherName, linkLesson):
		if self.__cursor:
			self.__cursor.execute("""INSERT INTO {}(
				"id",
				"date",
				"time_lesson",
				"subject_name",
				"description",
				"subgroup_number",
				"teacher_name",
				"link_lesson")
				VALUES(NULL, '{}', '{}', '{}', '{}', {}, '{}', '{}')""".format(tableName, date, timeLesson, subjectName, description, subgroupNumber, teacherName, linkLesson))
			self.__connection.commit()

	def getDataByDate(self, tableName, date):
		data = []
		if self.__cursor:
			for row in self.__cursor.execute("""SELECT * FROM {} WHERE date IN ('{}') ORDER BY time_lesson""".format(tableName, date)):
				data.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
		return data
	def clearData(self, tableName):
		if self.__cursor:
			self.__cursor.execute("""DELETE FROM {}""".format(tableName))
			self.__connection.commit()