from datetime import datetime
from flask import Blueprint, request
from security import logged_in_route
from bson import json_util
import json
from database.state_change import StateChange
from database import schedule
api = Blueprint("schedule", __name__, url_prefix='/schedule')


# Routes to modify the non repeating schedule
@api.route('/', methods=["GET"])
@logged_in_route
def get_schedule():
    result = StateChange.get_all()
    return json.dumps({"data": result}, default=json_util.default)


@api.route('/', methods=["POST"])
@logged_in_route
def add_schedule():
    result = StateChange.from_dictionary(request.get_json(force=True)).save()
    return json.dumps({"data": result}, default=json_util.default)


@api.route('/', methods=["DELETE"])
@logged_in_route
def remove_schedule():
    to_remove = request.get_json(force=True)
    result = schedule.remove({"_id": to_remove["_id"]})
    return json.dumps({"data": result}, default=json_util.default)
