from flask import Blueprint, request, Response
from security import logged_in_route
from bson import json_util
import json
from database.state_change_repeating import StateChangeRepeating
from database import repeating_schedule
api = Blueprint("schedule_repeating", __name__, url_prefix='/schedule/repeating')


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
