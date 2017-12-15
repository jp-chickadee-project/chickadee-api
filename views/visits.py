from flask import Blueprint, request, current_app

visits = Blueprint('visits', __name__)

@visits.route("/api/visits", methods=['GET', 'POST'])
def visitCollection():
	db = current_app.config['DATABASE']

	if request.method == "GET":
		start = request.args.get("start")
		end = request.args.get("end")

		return db.queryVisitRange(start, end)

	if request.method == 'POST':
		return db.queryAddRow("visits", request.form)