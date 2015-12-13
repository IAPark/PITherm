import argparse
import json
from datetime import datetime

from flask import Flask, Response
from src import state_changes
from src import state_changes_weekly

from src.state_changes import StateChange
from src.state_changes_weekly import StateChangeWeekly

parser = argparse.ArgumentParser(description='Record a Schedule of States both by exact time and by time of the week')
parser.add_argument("-p", "--port", type=int, help="the port to run server on", default=5003)
args = parser.parse_args()

app = Flask(__name__)

app.register_blueprint(state_changes.api)
app.register_blueprint(state_changes_weekly.api)

@app.route("/state/<time>")
def get_state(time: str):
    scheduled = StateChange.get_current(datetime.utcfromtimestamp(int(time)))
    if scheduled is not None:
        return Response(json.dumps({"data": scheduled.to_dictionary()["state"]}))

    repeating = StateChangeWeekly.get_current(datetime.utcfromtimestamp(int(time)))
    if repeating is not None:
        return Response(json.dumps({"data": repeating.to_dictionary()["state"]}))
    return Response(json.dumps({"data": None, "errors": ["can't find any scheduled states"]}))

if __name__ == "__main__":
    app.run(debug=True, port=args.port, host='0.0.0.0')
