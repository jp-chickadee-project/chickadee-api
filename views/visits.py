from flask import Blueprint, request, current_app, jsonify, Response

visits = Blueprint('visits', __name__)

#This is a messy, but I can't think of a cleaner way at the moment.
#Ideally all SQL syntax here would be abstracted to the ChickadeeDatabase class
@visits.route("/api/visits/", methods=['GET'])
def getVisits(limit=None):
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
	if start and end and not limit:
		if int(start) > int(end):
			return Response("Bad time-range specification", status=400)
		constraints.append("visitTimestamp BETWEEN %s AND %s" % (start, end))

	query = "SELECT * FROM visits "
	if constraints:
		query += "WHERE " + " AND ".join(constraints)
	query += " ORDER BY visitTimeStamp DESC "
	if limit:
		query += " LIMIT %s" % (limit)

	return jsonify(db.query(query + ";")), 200

@visits.route("/api/visits/", methods=['POST'])
def addVisit():
	db = current_app.config['DATABASE']

	if request.form["rfid"] and request.form["feederID"]:
		db.createRow("visits", request.form)
		return Response(request.form, status=200)

	return Response("Primary keys not properly supplied", status=400)

@visits.route("/api/visits/latest", methods=['GET'])
def getLatestVisits():
	limit = request.args.get("limit")
	return getVisits(limit if limit else 10)
