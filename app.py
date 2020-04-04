from flask import Flask
import requests

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello world!"


@app.route("/post", methods=["POST"])
def post():
    hoge = requests.form["hoge"]
    return hoge


# おまじない
if __name__ == '__main__':
    app.run()
