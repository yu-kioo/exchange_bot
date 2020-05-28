from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, make_response
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# user_defined
from average_candle_strategy.Manager import Manager
from average_candle_strategy.CommonParams import USD_JPY

app = Flask(__name__)

executor = ThreadPoolExecutor(max_workers=2)  # thread実行instance
jobs = {}
futures = {}


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
@app.route("/average_candle_strategy/start")
def start_avg_candle_strategy():
    avg_candle_strategy = Manager(USD_JPY)
    jobs["avg_candle_strategy"] = avg_candle_strategy
    future = executor.submit(avg_candle_strategy.run)
    futures["avg_candle_strategy"] = future
    return "start average_candle_strategy!"


@app.route("/average_candle_strategy/stop")
def stop_avg_candle_strategy():
    jobs["avg_candle_strategy"].status = False

    print(f"class status = {jobs['avg_candle_strategy'].status}")

    del(jobs["avg_candle_strategy"])
    futures["avg_candle_strategy"].cancel()

    result = "stop average_candle_strategy!" if futures["avg_candle_strategy"].done(
    ) else "running avg_candle_strategy"

    del(futures["avg_candle_strategy"])

    executor.shutdown(wait=False)

    return result


@app.route("/thread/running")
def running_threads():
    return jobs.keys


# おまじない
if __name__ == '__main__':
    app.run()
