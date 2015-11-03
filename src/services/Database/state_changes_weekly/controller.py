import json
from bson import json_util
from flask import Blueprint, Response, request
from flask.ext.cors import CORS
from model import StateChangeWeekly

api = Blueprint("state_changes_weekly", __name__, url_prefix='/schedule/repeating')
CORS(api)


@api.route('/', methods=["GET"])
def get():
    result = StateChangeWeekly.get_all_dic()
    return Response(json.dumps({"data": result}, default=json_util.default), mimetype='application/json')

@api.route('/current')
def get_current():
    return "not implemented"


@api.route('/', methods=["post"])
def add():
    result = StateChangeWeekly.from_dictionary(request.get_json(force=True)).save()
    return Response(json.dumps({"data": result}, default=json_util.default), mimetype='application/json')

@api.route('/', methods=["delete"])
def delete():
    to_remove = request.get_json(force=True)
    result = StateChangeWeekly.remove(to_remove['_id'])
    return Response(json.dumps({"data": result}, default=json_util.default), mimetype='application/json')