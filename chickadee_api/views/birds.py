from flask import Blueprint, request, current_app, jsonify, Response
from collections import defaultdict

birds = Blueprint('birds', __name__)

@birds.route("/<rfid>", methods=['GET'])
def getBird(rfid):
	db = current_app.config['DATABASE']

	if db.getRow("birds", rfid) == []:
		return Response("404 - Specified rfid does not exist", status=404);

	return jsonify(db.getRow("birds", rfid)), 200

@birds.route("/<rfid>", methods=['PUT', 'DELETE'])
def modifyBird(rfid):
	db = current_app.config['DATABASE']

	if db.getRow("birds", rfid) == []:
		return Response("404 - Specified rfid does not exist", status=404);

	if request.method == 'PUT':
		db.updateRow("birds", rfid, request.form)
		return jsonify(db.getRow("birds", rfid)), 201

	if request.method == 'DELETE':
		return jsonify(db.deleteRow("birds", rfid)), 204

@birds.route("/", methods=['GET'])
def getAllBirds():
	db = current_app.config['DATABASE']
	return jsonify(db.getTable("birds")), 200

@birds.route("/", methods=['POST'])
def addBird():
	db = current_app.config['DATABASE']

	if not request.form["rfid"]:
		return Response("rfid not supplied", status=400)

	form = defaultdict(lambda: "")
	for key, value in request.form.items():
		form[key] = value

	if "bandCombo" not in form:
		form["bandCombo"] = "%s%s/%s%s" % (
			form["legRightTop"], 
			form["legRightBottom"], 
			form["legLeftTop"], 
			form["legLeftBottom"]
		)
	db.createRow("birds", form)
	return jsonify(db.getRow("birds", form["rfid"])), 201


@birds.route("/options", methods=['GET'])
def birdOptions():
	db = current_app.config['DATABASE']

	options = {
		"species": db.getTable("birds", filters="DISTINCT species"),
		"captureSite": db.getTable("birds", filters="DISTINCT captureSite"),
		"tissueSample": db.getTable("birds", filters="DISTINCT tissueSample"),
		"suspectedSex":	db.getTable("birds", filters="DISTINCT suspectedSex"),
	}
	for key in options:
		options[key] = [options[key][x][key] for x in range(len(options[key]))]

	bands = db.getTable("bands")
	options["bands"] = {}
	for i, item in enumerate(bands):
		options["bands"][item["band"]] = item["description"]

	banders = db.getTable("birds", filters="DISTINCT banders")
	options["banders"] = [x["banders"] for x in banders]

	temp = set()
	for x in options["banders"]:
		if x:
			temp = temp | set(x.split(", "))
	options["banders"] = list(temp)

	return jsonify(options)
