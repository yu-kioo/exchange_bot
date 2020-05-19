import pandas as pd
import json
# candle情報の取得
import oandapyV20.endpoints.instruments as instruments
# 現在価格の取得
from oandapyV20.endpoints.pricing import PricingInfo
# 現在価格の取得(0.25秒の価格データを４つセットで返す)
from oandapyV20.endpoints.pricing import PricingStream
from oandapyV20 import API
from oandapyV20.exceptions import V20Error

# user defined
from CommonParams import ACCOUNT_ID, ACCESS_TOKEN, TRADE_ENV

"""
現在・過去価格の取得
"""


# TODO：ここcandleのデータのみを保持するdata_objと振る舞い分離した方がすっきりする？
class CandleStick:

    def __init__(self, instrument, time_frame):
        self.client = API(access_token=ACCESS_TOKEN, environment=TRADE_ENV)
        self.instrument = instrument
        self.config = {
            "params": {"granularity": time_frame, "count": 4, "price": "B"},
            "instrument": instrument,
        }
        self.fixed_candles = self.fixed_candle_df()
        self.avg_candles = self.avg_candle_df()

    # 現在価格のgenerator_objを返す
    def streaming_price(self):
        pricing_info = PricingStream(accountID=ACCOUNT_ID, params={
            "instruments": self.instrument})

        return self.client.request(pricing_info)

    # 過去のロウソク足データ取得
    def fixed_candle_df(self):
        data = self.__fixed_candle_data()
        self.fixed_candles = self.__cleaning_and_to_df(data)
        return self.__cleaning_and_to_df(data)

    # 平均足のデータ取得
    def avg_candle_df(self):
        # 1行目にnullデータを入れる
        data = [{"open": None, "high": None, "low": None, "close": None}]
        data.append(self.__first_avg_candle_row(
            self.fixed_candles.iloc[0], self.fixed_candles.iloc[1]))  # 最初の平均足
        # それ以降の平均足
        for i in range(2, len(self.fixed_candles)):
            data.append(self.__avg_candle_row(
                data[i - 1], self.fixed_candles.iloc[i]))
        # 作成した構造体をdfにする
        result = pd.DataFrame(data)
        result["time"] = self.fixed_candles["time"]
        self.avg_candles = result
        return result

    # #######
    # private
    # #######

    def __fixed_candle_data(self):
        instruments_candles = instruments.InstrumentsCandles(
            instrument=self.config["instrument"], params=self.config["params"])

        try:
            self.client.request(instruments_candles)
        except V20Error as e:
            print("Error: {}".format(e))

        return instruments_candles.response

    def __cleaning_and_to_df(self, data):  # df化と成形
        result = pd.json_normalize(data["candles"])

        result = result.rename(
            columns={"bid.o": "open", "bid.h": "high", "bid.l": "low", "bid.c": "close"})
        result = result.astype(
            {"open": float, "high": float, "low": float, "close": float})
        result["time"] = pd.to_datetime(result["time"])

        return result

    def __first_avg_candle_row(self, prev_row, self_row):
        # 引数は暗黙的に固定：prev_row df.iloc[0] , self_row = df.iloc[1]

        open = round(((prev_row["open"] + prev_row["high"] +
                       prev_row["low"] + prev_row["close"]) / 4), 3)
        high = self_row["high"]
        low = self_row["low"]
        close = round(((self_row["open"] + self_row["high"] +
                        self_row["low"] + self_row["close"]) / 4), 3)
        # TODO：python3.7以下ではdictの順序保持しないからorderDict使う？
        return {"open": open, "high": high, "low": low, "close": close}

    def __avg_candle_row(self, prev_row, self_row):
        # prev_row = １つ前の平均足、self_row = 自身のロウソク足

        open = round(((prev_row["open"] + prev_row["close"]) / 2), 3)
        close = round(((self_row["open"] + self_row["high"] +
                        self_row["low"] + self_row["close"]) / 4), 3)
        high = max([open, close, self_row["high"]])
        low = min([open, close, self_row["low"]])
        return {"open": open, "high": high, "low": low, "close": close}
