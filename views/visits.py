from flask import Blueprint, request, current_app, jsonify, Response

visits = Blueprint('visits', __name__)

@visits.route("/api/visits/", methods=['GET'])
def getVisits():
	db = current_app.config['DATABASE']

	start = request.args.get("start")
	end = request.args.get("end")
	rfid = request.args.get("rfid")
	feederID = request.args.get("feederID")

	constraints = []

	if rfid:
		constraints.append("rfid = '%s'" % (rfid))
	if feederID:
		constraints.append("feederID = '%s'" % (feederID))
	if start and end:
		if int(start) > int(end):
			return Response("Bad time-range specification", status=400)
		constraints.append("visitTimestamp BETWEEN %s AND %s" % (start, end))

	query = "SELECT * FROM visits "
	if constraints:
		query += "WHERE " + " AND ".join(constraints)

	return jsonify(db.query(query + " ORDER BY visitTimeStamp DESC;")), 200

@visits.route("/api/visits/", methods=['POST'])
def addVisit():
	db = current_app.config['DATABASE']

	if request.form["rfid"] and request.form["feederID"]:
		db.createRow("visits", request.form)
		return Response(request.form, status=200)

	return Response("Primary keys not properly supplied", status=400)

@visits.route("/api/visits/latest", methods=['GET'])
def getLatestVisits():
	db = current_app.config['DATABASE']

	rfid = request.args.get("rfid")
	feederID = request.args.get("feederID")
	limit = request.args.get("limit") if request.args.get("limit") else 10

	constraints = []

	if rfid:
		constraints.append("rfid = '%s'" % (rfid))
	if feederID:
		constraints.append("feederID = '%s'" % (feederID))

	query = "SELECT * FROM visits "
	if constraints:
		query += "WHERE " + " AND ".join(constraints)
	query += " ORDER BY visitTimeStamp DESC LIMIT %s;" % (limit)

	return jsonify(db.query(query)), 200
