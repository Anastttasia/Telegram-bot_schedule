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
				"date"	TEXT,
				"day_week"	TEXT,
				"number_lesson"	INTEGER,
				"subject_name"	TEXT,
				"subgroup_number"	INTEGER,
				"teacher_name"	TEXT)""".format(tableName))
			self.__connection.commit()

	def insertData(self, tableName, date, dayWeek, numberLesson, subjectName, subgroupNumber, teacherName):
		if self.__cursor:
			self.__cursor.execute("""INSERT INTO {}(
				"id",
				"date",
				"day_week",
				"number_lesson",
				"subject_name",
				"subgroup_number",
				"teacher_name")
				VALUES(NULL, '{}', '{}', {}, '{}', {}, '{}')""".format(tableName, date, dayWeek, numberLesson, subjectName, subgroupNumber, teacherName))
			self.__connection.commit()

	def updateData(self, tableName, nameField, newMeaning, searchField, searchMeaning):
		if self.__cursor:
			self.__cursor.execute("""UPDATE {} SET {} = '{}' WHERE {} LIKE '{}'""".format(tableName, nameField, newMeaning, searchField, searchMeaning))
			self.__connection.commit()


	def getDataByDate(self, tableName, date):
		if self.__cursor:
		
			for row in self.__cursor.execute("""SELECT * FROM {} WHERE date IN ('{}') ORDER BY number_lesson""".format(tableName, date)):
				rowId = row[0]
				date = row[1]
				dayWeek = row[2]
				numberLesson = row[3]
				subjectName = row[4]
				subgroupNumber = row[5]
				teacherName = row[6]
				print('rowId :: {}, date :: {}, dayWeek :: {}, numberLesson :: {}, subjectName :: {}, subgroupNumber :: {}, teacherName :: {}'.format(rowId, date, dayWeek, numberLesson, subjectName, subgroupNumber, teacherName))
