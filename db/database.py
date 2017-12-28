from flask_mysqldb import MySQL
import MySQLdb

class chickadeeDatabase():
	pri_keys = {
		"birds": "rfid",
		"feeders": "id",
	}

	def __init__(self):
		self.mysql = MySQL()

	def query(self, aQuery):
		cur = self.mysql.connection.cursor()

		try:
			cur.execute(aQuery)
		except (MySQLdb.Error) as e:
			return str(e)

		self.mysql.connection.commit()

		data = [dict((cur.description[i][0], value)
			for i, value in enumerate(row)) for row in cur.fetchall()]

		if len(data) == 1:
			data = data[0]
		return data

	def getTable(self, table, filters="*"):
		return self.query(
			"SELECT %s FROM %s;" 
				% (filters, table))

	def getVisitRange(self, start, end, field="", key=""):
		keyCondition = ""
		if key:
			keyCondition = "AND %s = '%s'" % (field, key)

		return self.query(
			"SELECT * FROM visits WHERE visitTimestamp BETWEEN %s AND %s %s;"
				% (start, end, keyCondition))

	def getRow(self, table, key):
		return self.query(
			"SELECT * FROM %s WHERE %s = '%s';" 
				% (table, self.pri_keys[table], key))

	def createRow(self, table, form):
		fields = ", ".join([key for key in form.keys()])
		values = "', '".join([val for val in form.values()])

		return self.query(
			"INSERT INTO %s (%s) VALUES ('%s');" 
				% (table, fields, values))

	def updateRow(self, table, key, form):
		form = ", ".join(["%s = '%s'" % (x, form[x]) for x in form])

		return self.query(
			"UPDATE %s SET %s WHERE %s = '%s'" 
				% (table, form, self.pri_keys[table], key))

	def deleteRow(self, table, key):
		self.query(
			"DELETE FROM %s WHERE %s = '%s';" 
				% (table, self.pri_keys[table], key))
		return {}