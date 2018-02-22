from flask import Blueprint, request, current_app, jsonify, Response
from collections import defaultdict

visits = Blueprint('visits', __name__)

#This is a messy, but I can't think of a cleaner way at the moment.
#Ideally all SQL syntax here would be abstracted to the ChickadeeDatabase class
@visits.route("/", methods=['GET'])
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
	elif not limit:
		return Response("Bad time-range specification", status=400)

	query = "SELECT * FROM visits "
	if constraints:
		query += "WHERE " + " AND ".join(constraints)
	query += " ORDER BY visitTimeStamp DESC "
	if limit:
		query += " LIMIT %s" % (limit)

	return jsonify(db.query(query + ";")), 200

@visits.route("/", methods=['POST'])
def addVisit():
	db = current_app.config['DATABASE']

	if not (request.form["rfid"] and request.form["feederID"]):
		return Response("Primary keys not properly supplied", status=400)

	form = defaultdict(lambda: "")
	for key, value in request.form.items():
		form[key] = value
	correspondingBird = db.getRow("birds", form["rfid"])

	form["bandCombo"] = correspondingBird["bandCombo"]
	db.createRow("visits", form)

	return Response(form, status=200)

@visits.route("/latest", methods=['GET'])
def getLatestVisits():
	limit = request.args.get("limit")
	return getVisits(limit if limit else 10)
