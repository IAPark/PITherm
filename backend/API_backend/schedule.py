__author__ = 'Isaac'
from backend import router
import services
from datetime import datetime

@router.route("/schedule/GET")
def get_schedule(body):
    return list(services.DB.schedule.find())


@router.route("/schedule/POST")
def get_schedule(body):
    start = datetime.utcfromtimestamp(body["start"])
    end = datetime.utcfromtimestamp(body["end"])

    print(type(body))
    print(start)

    AC_target = datetime["state"]["AC_target"]
    heater_target = datetime["state"]["heater_target"]
    fan = datetime["state"]["fan"]

    services.DB.set_delayed_state_change(start, end, AC_target, heater_target, fan)
