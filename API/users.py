from flask import Blueprint, request, Response
from security import logged_in_route
from bson import json_util
import json
from flask.ext.cors import CORS
api = Blueprint("schedule_repeating", __name__, url_prefix='/schedule/repeating')
CORS(api)


# Login
@api.route('/login', methods=["GET"])
@logged_in_route
def login():
    return Response(json.dumps({"data": "logged in"}, default=json_util.default), mimetype='application/json')


