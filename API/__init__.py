from flask import Flask
import schedule
import schedule_repeating
import user

app = Flask(__name__)

app.register_blueprint(schedule.api)
app.register_blueprint(schedule_repeating.api)
app.register_blueprint(user.api)
