from flask import Blueprint, request, current_app, jsonify

feeders = Blueprint('feeders', __name__)

@feeders.route("/api/feeders/<feederID>", methods=['GET', 'PUT', 'DELETE'])
def feedersByID(feederID):
	db = current_app.config['DATABASE']

	if db.getRow("feeders", feederID) == []:
		return Response(status=404);

	if request.method == "GET":
		resp, code = jsonify(db.getRow("feeders", feederID)), 200

	if request.method == 'PUT':
		db.updateRow("feeders", feederID, request.form)
		resp, code = jsonify(db.getRow("feeders", feederID)), 201

	if request.method == "DELETE":
		resp, code = jsonify(db.deleteRow("feeders", feederID)), 204

	resp.status_code = code
	return resp

@feeders.route("/api/feeders/", methods=['GET', 'POST'])
def feederCollection():
	db = current_app.config['DATABASE']

	if request.method == 'GET':
		resp, code = jsonify(db.getTable("feeders")), 200

	if request.method == 'POST':
		if request.form["id"]:
			db.createRow("feeders", request.form)
			resp, code = jsonify(db.getRow("feeders", request.form["id"])), 201
		else:
			resp, code = Response("id not supplied"), 400

	resp.status_code = code
	return resp