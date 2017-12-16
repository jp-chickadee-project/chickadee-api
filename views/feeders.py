from flask import Blueprint, request, current_app, jsonify

feeders = Blueprint('feeders', __name__)

@feeders.route("/api/feeders/<feederID>", methods=['GET', 'PUT', 'DELETE'])
def feedersByID(feederID):
	db = current_app.config['DATABASE']

	if request.method == "GET":
		start = request.args.get("start")
		end = request.args.get("end")

		if start and end:
			response = db.queryVisitRange(start, end, field="feederID", key=feederID)
		else:
			response = db.queryRow("feeders", "id", feederID)

	if request.method == 'PUT':
		response = db.queryUpdateRow("feeders", "id", feederID, request.form)

	if request.method == "DELETE":
		response = db.queryDeleteRow("feeders", "id", feederID)

	return jsonify(response)

@feeders.route("/api/feeders", methods=['GET', 'POST'])
def feederCollection():
	db = current_app.config['DATABASE']

	if request.method == 'GET':
		response = db.queryTable("feeders")

	if request.method == 'POST':
		response = db.queryAddRow("feeders", request.form)

	return jsonify(response)
