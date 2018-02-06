from flask import Blueprint, request, current_app, jsonify, Response

feeders = Blueprint('feeders', __name__)

@feeders.route("/api/feeders/<feederID>", methods=['GET'])
def getFeeder(feederID):
	db = current_app.config['DATABASE']

	if db.getRow("feeders", feederID) == []:
		return Response("404 - Specified feeder does not exist", status=404);

	return jsonify(db.getRow("feeders", feederID)), 200

	resp.status_code = code
	return resp

@feeders.route("/api/feeders/<feederID>", methods=['PUT', 'DELETE'])
def modifyFeeder(feederID):
	db = current_app.config['DATABASE']

	if db.getRow("feeders", feederID) == []:
		return Response("404 - Specified feeder does not exist", status=404);

	if request.method == 'PUT':
		db.updateRow("feeders", feederID, request.form)
		return jsonify(db.getRow("feeders", feederID)), 201

	if request.method == "DELETE":
		return jsonify(db.deleteRow("feeders", feederID)), 204


@feeders.route("/api/feeders/", methods=['GET'])
def getAllFeeders():
	db = current_app.config['DATABASE']
	return jsonify(db.getTable("feeders")), 200

@feeders.route("/api/feeders/", methods=['POST'])
def addFeeder():
	db = current_app.config['DATABASE']

	if not request.form["id"]:
		return Response("feederID not supplied", status=400)

	db.createRow("feeders", request.form)
	return jsonify(db.getRow("feeders", request.form["id"])), 201