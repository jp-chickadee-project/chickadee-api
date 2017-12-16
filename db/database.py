from flask_mysqldb import MySQL
import MySQLdb

class chickadeeDatabase():
	def __init__(self, app):
		self.mysql = MySQL()


	def query(self, aQuery):
		cur = self.mysql.connection.cursor()

		try:
			cur.execute(aQuery)
		except (MySQLdb.Error, MySQLdb.Warning) as e:
			return str(e), 400

		self.mysql.connection.commit()

		data = [dict((cur.description[i][0], value)
			for i, value in enumerate(row)) for row in cur.fetchall()]

		if len(data) == 1:
			data = data[0]
		return data


	def queryVisitRange(self, start, end, field="", key=""):
		keyCondition = ""
		if key:
			keyCondition = "visits.%s = '%s' AND" % (field, key)

		return self.query(
			"SELECT * FROM visits WHERE %s visitTimestamp BETWEEN %s AND %s;" %
			(keyCondition, start, end))

	def queryRow(self, table, field, key):
		return self.query("SELECT * FROM %s WHERE %s = '%s';" % (table, field, key))

	def queryAddRow(self, table, form):
		fields = ", ".join([key for key in form.keys()])
		values = "', '".join([val for val in form.values()])
		return self.query("INSERT INTO %s (%s) VALUES ('%s');" % (table, fields, values))

	def queryUpdateRow(self, table, field, key, form):
		form = ", ".join(["%s = '%s'" % (x, form[x]) for x in form])

		return self.query("UPDATE %s SET %s WHERE %s = '%s'" % (table, form, field, key))

	def queryTable(self, table):
		return self.query("SELECT * FROM %s;" % (table))

	def queryDeleteRow(self, table, field, key):
		return self.query("DELETE FROM %s WHERE %s = '%s';" % (table, field, key))