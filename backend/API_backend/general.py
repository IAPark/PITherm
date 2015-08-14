from backend import router
import services


@router.route("/temp")
def get_temp(body):
    return services.TempMonitor.last_temp


@router.route("/temps")
def get_temps(body):
    return list(services.DB.temps.find().sort([("date", 1)]))