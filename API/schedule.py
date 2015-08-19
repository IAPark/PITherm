from flask import Blueprint, request, Response
from flask.ext.cors import CORS
from security import logged_in_route
from bson import json_util
import json
from database.state_change import StateChange
from database import schedule
api = Blueprint("schedule", __name__, url_prefix='/schedule')
CORS(api)


# Routes to modify the non repeating schedule
@api.route('/', methods=["GET"])
@logged_in_route
def get_schedule():
    result = StateChange.get_all_dic()
    return Response(json.dumps({"data": result}, default=json_util.default), mimetype='application/json')


@api.route('/', methods=["POST"])
@logged_in_route
def add_schedule():
    result = StateChange.from_dictionary(request.get_json(force=True)).save()
    return Response(json.dumps({"data": result}, default=json_util.default), mimetype='application/json')


@api.route('/', methods=["DELETE"])
@logged_in_route
def remove_schedule():
    to_remove = StateChange.from_dictionary(request.get_json(force=True))
    result = schedule.remove({"_id": to_remove.id})
    return Response(json.dumps({"data": result}, default=json_util.default), mimetype='application/json')
