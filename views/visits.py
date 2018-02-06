from flask import Blueprint, request, current_app, jsonify, Response

visits = Blueprint('visits', __name__)

@visits.route("/api/visits/", methods=['GET'])
def getVisits():
	db = current_app.config['DATABASE']

	start = request.args.get("start")
	end = request.args.get("end")

	if start and end and int(start) < int(end):
		return jsonify(db.getVisitRange(start, end)), 200

	return Response("Bad time-range specification", status=400)

@visits.route("/api/visits/", methods=['POST'])
def addVisit():
	db = current_app.config['DATABASE']

	if request.form["rfid"] and request.form["feederID"]:
		db.createRow("visits", request.form)
		return Response(request.form, status=200)

	return Response("Primary keys not properly supplied", status=400)