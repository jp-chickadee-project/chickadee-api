from flask import Blueprint, request, current_app, jsonify, Response
from collections import defaultdict
import json

birds = Blueprint('birds', __name__)

@birds.route("/api/birds/<rfid>", methods=['GET', 'PUT', 'DELETE'])
def birdsByID(rfid):
	db = current_app.config['DATABASE']

	if db.getRow("birds", rfid) == []:
		return Response("404 - Specified rfid does not exist", status=404);

	if request.method == 'GET':
		resp, code = jsonify(db.getRow("birds", rfid)), 200

	if request.method == 'PUT':
		db.updateRow("birds", rfid, request.form)
		resp, code = jsonify(db.getRow("birds", rfid)), 201

	if request.method == "DELETE":
		resp, code = jsonify(db.deleteRow("birds", rfid)), 204

	resp.status_code = code
	return resp

@birds.route("/api/birds/", methods=['GET', 'POST'])
def birdCollection():
	db = current_app.config['DATABASE']

	if request.method == 'GET':
		resp, code = jsonify(db.getTable("birds")), 200

	if request.method == 'POST':
		if request.form["rfid"]:
			form = defaultdict(lambda: "")
			for key, value in request.form.items():
				form[key] = value

			form["bandCombo"] = "%s%s/%s%s" % (
				form["legRightTop"], 
				form["legRightBottom"], 
				form["legLeftTop"], 
				form["legLeftBottom"]
			)
			db.createRow("birds", form)
			resp, code = jsonify(db.getRow("birds", form["rfid"])), 201
		else:
			resp, code = Response("rfid not supplied", status=400)


	resp.status_code = code
	return resp


@birds.route("/api/birds/options", methods=['GET'])
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

	bands = db.getTable("bands")[:-1]
	temp = {}
	for i, item in enumerate(bands):
		temp[item["band"]] = item["description"]

	options["bands"] = temp

	banders = db.getTable("birds", filters="DISTINCT banders")
	options["banders"] = [x["banders"] for x in banders]

	temp = set()
	for x in options["banders"]:
		if x:
			temp = temp | set(x.split(", "))
	options["banders"] = list(temp)

	return jsonify(options)
