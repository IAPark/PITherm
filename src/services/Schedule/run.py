from flask import Flask
import state_changes
import state_changes_weekly

app = Flask(__name__)

app.register_blueprint(state_changes.api)
app.register_blueprint(state_changes_weekly.api)


if __name__ == "__main__":
    app.run(debug=True)