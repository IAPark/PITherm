import json

from flask import Blueprint, Response
from bson import json_util
from flask.ext.cors import CORS

from src.services.monolithic.services import logged_in_route

api = Blueprint("user", __name__, url_prefix='/user')
CORS(api)


# Login
@api.route('/')
@logged_in_route
def login():
    return Response(json.dumps({"data": "logged in"}, default=json_util.default), mimetype='application/json')


