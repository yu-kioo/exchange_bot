from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello world!"


@app.route("/post", methods=["POST"])
def post():
    # postのparamを取得
    hoge = request.form["hoge"]
    # getのparamの場合はこう
    # request.args.get("hoge")
    return f"postパラメータ：{hoge}"


# おまじない
if __name__ == '__main__':
    app.run()
