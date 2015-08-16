from flask import Blueprint, request, Response
from security import logged_in_route
from bson import json_util
import json
from database.state_change_repeating import StateChangeRepeating
from database import schedule
api = Blueprint("schedule_repeating", __name__, url_prefix='/schedule/repeating')


# Routes to modify the non repeating schedule
@api.route('/', methods=["GET"])
@logged_in_route
def get_schedule_repeating():
    result = StateChangeRepeating.get_all_dic()
    return Response(json.dumps({"data": result}, default=json_util.default), mimetype='application/json')


@api.route('/', methods=["POST"])
@logged_in_route
def add_schedule_repeating():
    print("in function")
    json = request.get_json(force=True)
    print(json)
    result = StateChangeRepeating.from_dictionary(json)
    print(result)
    result = result.save()
    print(result)
    return Response(json.dumps({"data": result}, default=json_util.default), mimetype='application/json')


@api.route('/', methods=["DELETE"])
@logged_in_route
def remove_schedule_repeating():
    to_remove = StateChangeRepeating.from_dictionary(request.get_json(force=True))
    result = schedule.remove({"_id": to_remove.id})
    return Response(json.dumps({"data": result}, default=json_util.default), mimetype='application/json')
