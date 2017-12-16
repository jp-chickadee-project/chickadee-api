from flask import Blueprint, request, current_app, jsonify
import json

birds = Blueprint('birds', __name__)

@birds.route("/api/birds/<rfid>", methods=['GET', 'PUT', 'DELETE'])
def birdsByID(rfid):
	db = current_app.config['DATABASE']
	if request.method == 'GET':
		start = request.args.get("start")
		end = request.args.get("end")

		if start and end:
			response = db.queryVisitRange(start, end, field="rfid", key=rfid)
		else:
			response = db.queryRow("birds", "rfid", rfid)

	if request.method == 'PUT':
		response = db.queryUpdateRow("birds", "rfid", rfid, request.form)

	if request.method == "DELETE":
		response = db.queryDeleteRow("birds", "rfid", rfid)

	return jsonify(response)

@birds.route("/api/birds", methods=['GET', 'POST'])
def birdCollection():
	db = current_app.config['DATABASE']

	if request.method == 'GET':
		response = db.queryTable("birds")

	if request.method == 'POST':
		response = db.queryAddRow("birds", request.form)

	return jsonify(response)


@birds.route("/api/birds/options", methods=['GET'])
def birdOptions():
	db = current_app.config['DATABASE']

	options = {
		"species": db.query("SELECT DISTINCT species FROM birds;")[:-1],
		"captureSite": db.query("SELECT DISTINCT captureSite FROM birds;")[:-1],
		"tissueSample": db.query("SELECT DISTINCT tissueSample FROM birds;")[:-1],
		"suspectedSex":	db.query("SELECT DISTINCT suspectedSex FROM birds;")[:-1]
	}

	legs = {
		"legLeftBottom": db.query("SELECT DISTINCT legLeftBottom FROM birds;")[:-1],
		"legLeftTop": db.query("SELECT DISTINCT legLeftTop FROM birds;")[:-1],
		"legRightBottom": db.query("SELECT DISTINCT legRightBottom FROM birds;")[:-1],
		"legRightTop": db.query("SELECT DISTINCT legRightTop FROM birds;")[:-1]
	}
	banders = db.query("SELECT DISTINCT banders FROM birds;")[:-1]


	for key in options:
		options[key] = [options[key][x][key] for x in range(len(options[key]))]
	for key in legs:
		legs[key] = [legs[key][x][key] for x in range(len(legs[key]))]

	options["legs"] = list(
			set(legs["legLeftBottom"])	| 
			set(legs["legLeftTop"]) 	| 
			set(legs["legRightTop"])	| 
			set(legs["legRightBottom"])
		)

	options["banders"] = [x["banders"] for x in banders]
	temp = set()
	for x in options["banders"]:
		if x:
			temp = temp | set(x.split(", "))
	options["banders"] = list(temp)

	return jsonify(options)