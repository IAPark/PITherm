from datetime import datetime
from flask import Blueprint, request
from security import logged_in_route
from bson import json_util
import json
api = Blueprint("schedule", __name__, url_prefix='/schedule')

from services.database import DB
db = DB()



# Routes to modify the non repeating schedule
@api.route('/', methods=["GET"])
@logged_in_route
def get_schedule():
    result = list(db.schedule.find())
    for schedule in result:
        schedule["start"] = int(schedule["start"].strftime("%s"))
        schedule["end"] = int(schedule["end"].strftime("%s"))

    return json.dumps({"data": result}, default=json_util.default)


@api.route('/', methods=["POST"])
@logged_in_route
def add_schedule():
    to_add = request.get_json(force=True)
    start = datetime.utcfromtimestamp(to_add["start"])
    end = datetime.utcfromtimestamp(to_add["end"])

    AC_target = to_add["state"]["AC_target"]
    heater_target = to_add["state"]["heater_target"]
    fan = to_add["state"]["fan"]
    result = db.set_delayed_state_change(start, end, AC_target, heater_target, fan)
    return json.dumps({"data": result}, default=json_util.default)


@api.route('/', methods=["DELETE"])
@logged_in_route
def remove_schedule():
    to_remove = request.get_json(force=True)
    result = db.schedule.remove({"_id": to_remove["_id"]["$oid"]})
    return json.dumps({"data": result}, default=json_util.default)
