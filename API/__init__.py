from flask import Flask
import schedule
import schedule_repeating

app = Flask(__name__)

app.register_blueprint(schedule.api)
#app.register_blueprint(schedule_repeating.api)
