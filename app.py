from flask import Flask, request, make_response
import threading
from datetime import datetime
from time import sleep

app = Flask(__name__)


class Mythread(threading.Thread):
    def __init__(self):
        super(Mythread, self).__init__()
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        try:
            # ここで処理を継続実行する
            # Manage.new().run()
            while not self.stop_event.is_set():
                print(datetime.now())
                sleep(3)
        finally:
            print("***** thread process end *****")


jobs = {}


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


# thread実行群
@app.route("/start/<id>/")
def start(id):
    thread = Mythread()
    thread.start()
    jobs[id] = thread
    return make_response(f'{id}の処理を受け付けました\n'), 202


@app.route("/stop/<id>/")
def stop(id):
    jobs[id].stop()
    del jobs[id]
    return make_response(f'{id}の中止処理を受け付けました\n'), 202


@app.route("/status/<id>/")
def status(id):
    if id in jobs:
        return make_response(f'{id}は実行中です\n'), 200
    else:
        return make_response(f'{id}は実行していません\n'), 200


# おまじない
if __name__ == '__main__':
    app.run()
