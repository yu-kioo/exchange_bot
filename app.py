from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello world!"


@app.route("/post", methods=["POST"])
def post():
    # postのparamを取得
    obj = request.get_data()
    # getのparamの場合はこう
    # request.args.get("hoge")
    return f"request:{obj}, : {type(obj)}"


# おまじない
if __name__ == '__main__':
    app.run()
