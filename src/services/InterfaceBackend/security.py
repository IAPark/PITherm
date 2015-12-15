from functools import wraps
import json
from pymongo import MongoClient
from flask import request, Response

client = MongoClient()
users = client.PITherm.users


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


def valid_user(username, password):
    user = users.find_one({"username": username})
    if user is None:
        return False

    if not user["password"] == password:
        return False
    return True


bad_auth_message = Response(
    json.dumps({"error": ["bad login"]}), 401)


# Thanks to Armin Ronacher and his example at http://flask.pocoo.org/snippets/8/
def logged_in_route(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not valid_user(auth.username, auth.password):
            return bad_auth_message
        return function(*args, **kwargs)

    return wrapper
