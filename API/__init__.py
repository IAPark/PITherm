from flask import Flask
import schedule
import schedule_repeating
from services.database import DB

app = Flask(__name__)

app.register_blueprint(schedule.api)
app.register_blueprint(schedule_repeating.api)
db = DB()
