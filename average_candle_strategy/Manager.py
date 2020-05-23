import pandas as pd
import json
from oandapyV20.exceptions import V20Error

# user defined
# TODO：pathの書き方
from average_candle_strategy.CommonParams import USD_JPY, BUY, SELL
from average_candle_strategy.CandleStick import CandleStick
from average_candle_strategy.OrderData import OrderData
from average_candle_strategy.Strategy import Strategy
from average_candle_strategy.Trader import Trader

"""
一連のトレード処理を組み立てる
"""


class Manager:
    # TODO：可変的にする?
    LOT = 1000

    def __init__(self, instrument):
        self.status = True
        # 他のクラスのインスタンスを生成
        self.candle_stick = CandleStick(USD_JPY, "M5")
        self.strategy = Strategy()
        self.trader = Trader()

    def run(self):
        while self.status:
            try:
                for line in self.candle_stick.streaming_price():
                    if ("bids" in line):  # 価格が更新されてたら

                        if self.trader.has_open_positions():
                            continue

                        # TODO：データ更新の実行はエントリー足の間隔でいい
                        # fixed_candle, avg_candleのデータ更新
                        self.candle_stick.fixed_candle_df()
                        self.candle_stick.avg_candle_df()

                        print("exec strategy")

                        # エントリー可能な場合、ポジション発注
                        if self.__can_entry():
                            self.__log("entry")
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
        e_price = self.strategy.entry_price(self.candle_stick.avg_candles)
        p_price = self.strategy.profit_price(self.candle_stick.avg_candles)
        l_price = self.strategy.loss_cut_price(self.candle_stick.avg_candles)

        # 発注
        self.trader.order(OrderData(USD_JPY, BUY, self.LOT).limit_order(
            e_price["buy"], p_price["buy"], l_price["buy"])).order()
        self.trader.order(OrderData(USD_JPY, BUY, self.LOT).limit_order(
            e_price["sell"], p_price["sell"], l_price["sell"])).order()

    # TODO；logみたいなのに置き換える
    def __log(self, msg):
        print("******")
        print("{msg}")
        print("******")
