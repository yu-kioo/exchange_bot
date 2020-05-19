import pandas as pd
import json
from oandapyV20.exceptions import V20Error

# user defined
from CommonParams import USD_JPY
from CandleStick import CandleStick
from Strategy import Strategy

"""
一連のトレード処理を組み立てる
"""


class Manager:

    def __init__(self, instrument):
        # 自身のparams
        # トレード環境：ENVIRONMENT
        # debug環境(休日のAPI使えない時間用に用意しときたいなー感)

        # 他のクラスのインスタンスを生成
        self.candle_stick = CandleStick(USD_JPY, "M5")
        self.strategy = Strategy()

    def run(self):
        while True:
            try:
                for line in self.candle_stick.streaming_price():
                    if ("bids" in line):  # 価格が更新されてたら

                        # TODO：データ更新の実行はエントリー足の間隔でいい
                        # fixed_candle, avg_candleのデータ更新
                        self.candle_stick.fixed_candle_df()
                        self.candle_stick.avg_candle_df()

                        # エントリー判定・実行・決済
                        print("exec strategy")

                        # エントリー可能な場合、ポジション発注
                        if self.__can_entry():
                            self.__entry()

            except V20Error as e:
                print("Error! continue process....")
                print(e)
                pass

    # #######
    # private
    # #######

    # strategyの判定実行
    def __can_entry(self):
        return self.strategy.is_multi_diversion(self.candle_stick.avg_candles)

    # entry実行
    def __entry(self):
        entry_price = self.strategy.entry_price(
            self.candle_stick.avg_candles)
        high = entry_price["high"]
        low = entry_price["low"]

        # ターゲットライン
