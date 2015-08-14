__author__ = 'Isaac'
from backend import router
import services


@router.route("/schedule/GET")
def get_schedule(body):
    return list(services.DB.schedule.find())


@router.route("/schedule/POST")
def get_schedule(body):
    print(body)
