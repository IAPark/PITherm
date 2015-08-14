__author__ = 'Isaac'
from backend import router
import services
from datetime import datetime


@router.route("/schedule/GET")
def get_schedule(body):
    return list(services.DB.schedule.find())


@router.route("/schedule/POST")
def post_schedule(body):
    start = datetime.utcfromtimestamp(body["start"])
    end = datetime.utcfromtimestamp(body["end"])

    AC_target = body["state"]["AC_target"]
    heater_target = body["state"]["heater_target"]
    fan = body["state"]["fan"]

    services.DB.set_delayed_state_change(start, end, AC_target, heater_target, fan)
    return {}


@router.route("/schedule/DELETE")
def delete_schedule(body):
    return services.DB.schedule.remove({"_id": body["_id"]["$oid"]})

