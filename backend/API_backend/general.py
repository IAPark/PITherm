from backend import router
import services
from database.temp_log import TempLog

@router.route("/temp")
def get_temp(body):
    return services.TempMonitor.last_temp
