from flask import Blueprint, request
from shared_funcs import *

visits = Blueprint('visits', __name__, template_folder='templates')

@visits.route("/api/visits", methods=['GET', 'POST'])
def visitCollection():
	if request.method == "GET":
		start = request.args.get("start")
		end = request.args.get("end")

		return queryVisitRange(start, end)

	if request.method == 'POST':
		return queryAddRow("visits", request.form)