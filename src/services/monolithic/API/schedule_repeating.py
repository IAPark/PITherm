import json

from flask import Blueprint, request, Response
from bson import json_util
from flask.ext.cors import CORS

from src.services.monolithic.services import logged_in_route
from src.services.database import StateChangeRepeating
from src.services.database import repeating_schedule

api = Blueprint("schedule_repeating", __name__, url_prefix='/schedule/repeating')
CORS(api)

# Routes to modify the non repeating schedule
@api.route('/', methods=["GET"])
@logged_in_route
def get_schedule():
    result = StateChangeRepeating.get_all_dic()
    return Response(json.dumps({"data": result}, default=json_util.default), mimetype='application/json')


@api.route('/', methods=["POST"])
@logged_in_route
def add_schedule():
    result = StateChangeRepeating.from_dictionary(request.get_json(force=True)).save()
    return Response(json.dumps({"data": result}, default=json_util.default), mimetype='application/json')


@api.route('/', methods=["DELETE"])
@logged_in_route
def remove_schedule():
    to_remove = StateChangeRepeating.from_dictionary(request.get_json(force=True))
    result = repeating_schedule.remove({"_id": to_remove.id})
    return Response(json.dumps({"data": result}, default=json_util.default), mimetype='application/json')
