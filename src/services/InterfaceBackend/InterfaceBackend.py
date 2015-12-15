from flask import Flask, Response, request
import flask
import argparse
import requests
from flask.ext.cors import CORS
from security import logged_in_route

parser = argparse.ArgumentParser(description='Interface Backend')
parser.add_argument("-p", "--port", type=int, help="the port to run server on", default=80)
parser.add_argument("-s", "--schedule", type=str, help="the url of the schedule service", default="http://localhost:5003")
args = parser.parse_args()

app = Flask(__name__)
CORS(app)

@app.route("/schedule/weekly/")
@logged_in_route
def get_weekly_schedule():
    response = requests.get(args.schedule + "/schedule/weekly/")
    return Response(response.text, mimetype=response.headers["Content-Type"])


@app.route("/schedule/weekly/", methods=["DELETE"])
@logged_in_route
def delete_weekly_schedule():
    response = requests.delete(args.schedule + "/schedule/weekly/", data=request.get_data(), headers=request.headers)
    return Response(response.text, mimetype=response.headers["Content-Type"])


@app.route("/schedule/weekly/", methods=["POST"])
@logged_in_route
def post_weekly_schedule():
    response = requests.post(args.schedule + "/schedule/weekly/", data=request.get_data(), headers=request.headers)
    return Response(response.text, mimetype=response.headers["Content-Type"])


@app.route("/schedule/")
@logged_in_route
def get_schedule():
    response = requests.get(args.schedule + "/schedule/")
    return Response(response.text, mimetype=response.headers["Content-Type"])


@app.route("/schedule/", methods=["DELETE"])
@logged_in_route
def delete_schedule():
    response = requests.delete(args.schedule + "/schedule/", data=request.get_data(), headers=request.headers)
    return Response(response.text, mimetype=response.headers["Content-Type"])


@app.route("/schedule/", methods=["POST"])
@logged_in_route
def post_schedule():
    response = requests.post(args.schedule + "/schedule/", data=request.get_data(), headers=request.headers)
    return Response(response.text, mimetype=response.headers["Content-Type"])


@app.route("/user/")
@logged_in_route
def valid_user():
    return flask.jsonify({"logged_in": True})

if __name__ == "__main__":
    app.run(debug=True, port=args.port, host='0.0.0.0')
