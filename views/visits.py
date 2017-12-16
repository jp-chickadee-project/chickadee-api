from flask import Blueprint, request, current_app, jsonify

visits = Blueprint('visits', __name__)

@visits.route("/api/visits", methods=['GET', 'POST'])
def visitCollection():
	db = current_app.config['DATABASE']

	if request.method == "GET":
		start = request.args.get("start")
		end = request.args.get("end")

		response = db.queryVisitRange(start, end)

	if request.method == 'POST':
		response = db.queryAddRow("visits", request.form)

	return jsonify(response)