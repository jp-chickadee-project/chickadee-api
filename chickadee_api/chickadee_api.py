from flask import Blueprint, current_app, request

import traceback

from .util import log

main = Blueprint('main', __name__)

@main.after_request
def after_request(response):
	if "LOGGER" not in current_app.config:
		return response
	if response.status_code != 500:
		log(current_app.config["LOGGER"], request, response.status)
	return response

@main.errorhandler(Exception)
def exceptions(e):
	backtrace = "500 INTERNAL SERVER ERROR\n" + traceback.format_exc()
	log(current_app.config["LOGGER"], request, backtrace)
	return "Internal Server Error", 500