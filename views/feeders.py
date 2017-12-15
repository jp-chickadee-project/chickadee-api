from flask import Blueprint, request, current_app

feeders = Blueprint('feeders', __name__)

@feeders.route("/api/feeders/<feederID>", methods=['GET', 'PUT', 'DELETE'])
def feedersByID(feederID):
	db = current_app.config['DATABASE']

	if request.method == "GET":
		start = request.args.get("start")
		end = request.args.get("end")

		if start and end:
			return db.queryVisitRange(start, end, field="feederID", key=feederID)
		else:
			return db.queryRow("feeders", "id", feederID)

	if request.method == "DELETE":
		return db.queryDeleteOne("feeders", "id", feederID)

@feeders.route("/api/feeders", methods=['GET', 'POST'])
def feederCollection():
	db = current_app.config['DATABASE']

	if request.method == 'GET':
		return db.queryTable("feeders")

	if request.method == 'POST':
		return db.queryAddRow("feeders", request.form)
