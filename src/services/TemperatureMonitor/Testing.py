from flask import Flask, Response, Request, request

app = Flask(__name__)

@app.route("/test", methods=["POST", "GET"])
def print_temp():
    print(request.json)
    return "Hello World"


if __name__ == "__main__":
    app.run(debug=True, port=1003, host='0.0.0.0')
