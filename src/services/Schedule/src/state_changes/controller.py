import json
from bson import json_util
from flask import Blueprint, Response, request
from flask.ext.cors import CORS
from .model import StateChange
from datetime import datetime


api = Blueprint("state_changes", __name__, url_prefix='/schedule')
CORS(api)


@api.route('/', methods=["GET"])
def get():
    result = StateChange.get_all_dic()
    return Response(json.dumps({"data": result}, default=json_util.default), mimetype='application/json')


@api.route('/current')
def get_current():
    current = StateChange.get_current(datetime.utcnow())

    if current is None:
        return Response(json.dumps({"data": None, "error": ["can't find"]},
                                   default=json_util.default), mimetype='application/json')

    return Response(json.dumps({"data": current.to_dictionary()}, default=json_util.default), mimetype='application/json')

@api.route('/next')
def get_next():
    next = StateChange.get_next(datetime.utcnow())

    if next is None:
        return Response(json.dumps({"data": None, "error": ["can't find"]},
                                   default=json_util.default), mimetype='application/json')

    return Response(json.dumps({"data": next.to_dictionary()}, default=json_util.default), mimetype='application/json')

@api.route('/', methods=["post"])
def add():
    result = StateChange.from_dictionary(request.get_json(force=True)).save()
    return Response(json.dumps({"data": result}, default=json_util.default), mimetype='application/json')

@api.route('/', methods=["delete"])
def delete():
    to_remove = request.get_json(force=True)
    result = StateChange.remove(to_remove['_id'])
    return Response(json.dumps({"data": result}, default=json_util.default), mimetype='application/json')