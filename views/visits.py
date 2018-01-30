from flask import Blueprint, request, current_app, jsonify, Response

visits = Blueprint('visits', __name__)

@visits.route("/api/visits/", methods=['GET', 'POST'])
def visitCollection():
	db = current_app.config['DATABASE']

	if request.method == "GET":
		start = request.args.get("start")
		end = request.args.get("end")

		if start and end and int(start) < int(end):
			keys = {
				"rfid": request.args.get("rfid"),
				"feederID": request.args.get("feederID")
			}
			resp, code = jsonify(db.getVisitRange(start, end, keys)), 200
		else:
			resp, code = Response("Bad time-range specification"), 400

	if request.method == 'POST':
		if request.form["rfid"] and request.form["feederID"]:
			db.createRow("visits", request.form)
			resp, code = Response(request.form), 200
		else:
			resp, code = Response("Primary keys not supplied"), 400

	resp.status_code = code
	return resp