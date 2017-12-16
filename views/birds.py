from flask import Blueprint, request, current_app, jsonify
import json

birds = Blueprint('birds', __name__)

@birds.route("/api/birds/<rfid>", methods=['GET', 'PUT', 'DELETE'])
def birdsByID(rfid):
	db = current_app.config['DATABASE']

	start = request.args.get("start")
	end = request.args.get("end")

	if start and end:
		return db.queryVisitRange(start, end, field="rfid", key=rfid)
	else:
		return db.queryRow("birds", "rfid", rfid)

	if request.method == "DELETE":
		return db.queryDeleteOne("birds", "rfid", rfid)

@birds.route("/api/birds/", methods=['GET', 'POST'])
def birdCollection():
	db = current_app.config['DATABASE']

	if request.method == 'GET':
		return db.queryTable("birds")

	if request.method == 'POST':
		return db.queryAddRow("birds", request.form)

@birds.route("/api/birds/options", methods=['GET'])
def birdOptions():
	db = current_app.config['DATABASE']

	def formatResponse(aQuery):
		response = db.query(aQuery)
		return json.loads(response.get_data())[:-1]

	options = {
		"species": formatResponse("SELECT DISTINCT species FROM birds;"),
		"captureSite": formatResponse("SELECT DISTINCT captureSite FROM birds;"),
		"tissueSample": formatResponse("SELECT DISTINCT tissueSample FROM birds;"),
		"suspectedSex":	formatResponse("SELECT DISTINCT suspectedSex FROM birds;")
	}

	legs = {
		"legLeftBottom": formatResponse("SELECT DISTINCT legLeftBottom FROM birds;"),
		"legLeftTop": formatResponse("SELECT DISTINCT legLeftTop FROM birds;"),
		"legRightBottom": formatResponse("SELECT DISTINCT legRightBottom FROM birds;"),
		"legRightTop": formatResponse("SELECT DISTINCT legRightTop FROM birds;")
	}
	banders = formatResponse("SELECT DISTINCT banders FROM birds;")


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