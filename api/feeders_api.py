from flask import Blueprint, render_template, abort, request, jsonify
from extensions import query

feeders = Blueprint('feeders', __name__, template_folder='templates')


@feeders.route("/api/feeders/<feederID>", methods=['GET', 'PUT', 'DELETE'])
def feedersByID(feederID):
	if request.method == "GET":
		start = request.args.get("start")
		end = request.args.get("end")
		if start and end:
			return jsonify(query(
				"SELECT * FROM visits \
					WHERE feederID = '{0}' \
					AND visitTimestamp BETWEEN {1} AND {2};".format(feederID, start, end)))
		else:
			return jsonify(query(
				"SELECT * FROM feeders \
					WHERE id = '{0}';".format(feederID)))

	if request.method == "DELETE":
		return jsonify(query(
			"DELETE FROM feeders\
				WHERE feederID = '{0}'"))


@feeders.route("/api/feeders", methods=['GET', 'POST'])
def feederCollection():
	if request.method == 'GET':
		feederID = request.args.get("feederID")
		if feederID:
			return feedersByID(feederID)
		else:
			return jsonify(query("SELECT * FROM feeders"))
