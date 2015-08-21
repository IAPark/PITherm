from flask import Blueprint, Response
from security import logged_in_route
from bson import json_util
import json
from flask.ext.cors import CORS
api = Blueprint("user", __name__, url_prefix='/user/')
CORS(api)


# Login
@api.route('/login')
@logged_in_route
def login():
    return Response(json.dumps({"data": "logged in"}, default=json_util.default), mimetype='application/json')


