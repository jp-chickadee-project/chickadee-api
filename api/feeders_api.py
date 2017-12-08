from flask import Blueprint, request
from shared_funcs import *

feeders = Blueprint('feeders', __name__, template_folder='templates')

@feeders.route("/api/feeders/<feederID>", methods=['GET', 'PUT', 'DELETE'])
def feedersByID(feederID):
	if request.method == "GET":
		start = request.args.get("start")
		end = request.args.get("end")

		if start and end:
			return queryVisitRange(start, end, field="feederID", key=feederID)
		else:
			return queryRow("feeders", "id", feederID)

	if request.method == "DELETE":
		return queryDeleteOne("feeders", feederID)


@feeders.route("/api/feeders", methods=['GET', 'POST'])
def feederCollection():
	if request.method == 'GET':
		feederID = request.args.get("feederID")
		if feederID:
			return feedersByID(feederID)
		else:
			return queryTable("feeders")
