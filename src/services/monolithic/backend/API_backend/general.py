from src.services.backend import router
from src.services import services


@router.route("/temp")
def get_temp(body):
    return services.TempMonitor.last_temp
