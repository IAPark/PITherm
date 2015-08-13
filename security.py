from functools import wraps
import json

__author__ = 'Isaac'
from flask import request, Response
from services.database import DB

db = DB()
users = db.client.PITherm.users

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


def valid_user(username, password):
    user = users.find_one({"username": username})
    if not user["password"] == password:
        return None
    return user


bad_auth_message = Response(
    json.dumps({"error": ["bad login"]}), 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def logged_in_route(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not valid_user(auth.username, auth.password):
            return bad_auth_message
        return function(*args, **kwargs)