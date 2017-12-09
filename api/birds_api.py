from flask import Blueprint, request, jsonify
from shared_funcs import *

birds = Blueprint('birds', __name__, template_folder='templates')


@birds.route("/api/birds/<rfid>", methods=['GET'])
def birdsByID(rfid):
	start = request.args.get("start")
	end = request.args.get("end")

	if start and end:
		return queryVisitRange(start, end, field="rfid", key=rfid)
	else:
		return queryRow("birds", "rfid", rfid)

@birds.route("/api/birds/", methods=['GET', 'POST'])
def birdCollection():
	if request.method == 'GET':
		rfid = request.args.get("rfid")
		if rfid:
			return birdsByID(rfid)
		return queryTable("birds")

	if request.method == 'POST':
		return queryAddRow("birds", request.form)

@birds.route("/api/birds/options", methods=['GET'])
def birdOptions():
	options = {
		"species": query("SELECT DISTINCT species FROM birds;"),
		"captureSite": query("SELECT DISTINCT captureSite FROM birds;"),
		"tissueSample": query("SELECT DISTINCT tissueSample FROM birds;"),
		"suspectedSex":	query("SELECT DISTINCT suspectedSex FROM birds;")
	}

	legs = {
		"legLeftBottom": query("SELECT DISTINCT legLeftBottom FROM birds;"),
		"legLeftTop": query("SELECT DISTINCT legLeftTop FROM birds;"),
		"legRightBottom": query("SELECT DISTINCT legRightBottom FROM birds;"),
		"legRightTop": query("SELECT DISTINCT legRightTop FROM birds;")
	}
	banders = query("SELECT DISTINCT banders FROM birds;")


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
		temp = temp | set(x.split(", "))
	options["banders"] = list(temp)

	return jsonify(options)
