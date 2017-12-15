from flask import Blueprint, request, current_app, g

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

	options = {
		"species": db.query("SELECT DISTINCT species FROM birds;"),
		"captureSite": db.query("SELECT DISTINCT captureSite FROM birds;"),
		"tissueSample": db.query("SELECT DISTINCT tissueSample FROM birds;"),
		"suspectedSex":	db.query("SELECT DISTINCT suspectedSex FROM birds;")
	}

	legs = {
		"legLeftBottom": db.query("SELECT DISTINCT legLeftBottom FROM birds;"),
		"legLeftTop": db.query("SELECT DISTINCT legLeftTop FROM birds;"),
		"legRightBottom": db.query("SELECT DISTINCT legRightBottom FROM birds;"),
		"legRightTop": db.query("SELECT DISTINCT legRightTop FROM birds;")
	}
	banders = db.query("SELECT DISTINCT banders FROM birds;")


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
