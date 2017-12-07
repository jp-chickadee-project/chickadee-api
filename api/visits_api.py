from flask import Blueprint, render_template, abort, request, jsonify
from extensions import app, query

visits = Blueprint('visits', __name__, template_folder='templates')

@visits.route("/api/visits", methods=['GET', 'POST'])
def visitCollection():
	if request.method == "GET":
		start = request.args.get("start")
		end = request.args.get("end")
		return jsonify(query(
			"SELECT * FROM visits "
			"WHERE visits.visitTimestamp "
			"BETWEEN " + start + " AND " + end + ";"))
