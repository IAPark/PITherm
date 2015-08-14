from flask import Blueprint, request
from security import logged_in_route
from bson import json_util
import json
from API_to_backend import command_queue, response_queue, get_for
api = Blueprint("schedule", __name__, url_prefix='/schedule')


# Routes to modify the non repeating schedule
@api.route('/', methods=["GET"])
@logged_in_route
def get_schedule():
    command_queue.put({"url": request.path + request.method, "body": request.get_json()})
    result = get_for(request.path + request.method, response_queue, 5)
    for schedule in result:
        schedule["start"] = int(schedule["start"].strftime("%s"))
        schedule["end"] = int(schedule["end"].strftime("%s"))

    return json.dumps({"data": get_for(request.path + request.method, response_queue, 5)}, default=json_util.default)


@api.route('/', methods=["POST"])
@logged_in_route
def add_schedule():
    command_queue.put({"url": request.path + request.method, "body": request.get_json()})
    return json.dumps({"data": get_for(request.path + request.method, response_queue, 5)}, default=json_util.default)


@api.route('/', methods=["DELETE"])
@logged_in_route
def remove_schedule():
    command_queue.put({"url": request.path + request.method, "body": request.get_json()})
    return json.dumps({"data": get_for(request.path + request.method, response_queue, 5)}, default=json_util.default)
