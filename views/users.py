from flask import Blueprint, request, current_app, jsonify, Response

users = Blueprint('users', __name__)

@users.route("/api/users", methods=['GET', 'POST', 'PUT', 'DELETE'])
def usersByName():
	db = current_app.config['DATABASE']
	username, pwHash = "", ""

	try:
		username = request.headers['username']
	except KeyError as e:
		return Response("username not provided", status=400)
	try: 
		pwHash = request.headers['password']
	except KeyError as e:
		pass

	username = "butt"
	if request.method == "GET":
		resp, code = jsonify(db.getRow("users", username)), 200

	if request.method == "POST":
		db.createRow("users", request.form)
		resp, code = jsonify(db.getRow("users", username)), 201

	if request.method == 'PUT':
		db.updateRow("users", feederID, request.form)
		resp, code = jsonify(db.getRow("users", username)), 201

	if request.method == "DELETE":
		resp, code = jsonify(db.deleteRow("users", username)), 204

	resp.status_code = code
	return resp