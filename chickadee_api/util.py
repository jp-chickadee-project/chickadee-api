from flask.json import JSONEncoder

import logging
import traceback
import datetime
import decimal
from time import strftime

class CustomJSONEncoder(JSONEncoder):
	def default(self, obj):
		try:
			if isinstance(obj, datetime.date) or isinstance(obj, datetime.timedelta) or isinstance(obj, datetime.datetime):
				return str(obj)
			if isinstance(obj, decimal.Decimal):
				return float(obj)
			iterable = iter(obj)
		except TypeError:
			pass
		else:
			return list(iterable)
		return JSONEncoder.default(self, obj)

def log(logger, request, message):
	timestamp = strftime('[%Y-%b-%d %H:%M:%S]')
	logger.info('%s %s %s %s %s %s',
		timestamp,
		request.remote_addr,
		request.method,
		request.scheme,
		request.full_path,
		message)