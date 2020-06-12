import pandas as pd
import json
import time as t
from datetime import datetime, date, time, timedelta, timezone
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
        while not self.__is_market_open():
            self.__wait_while_market_close()
            continue
        self.status = True
        self.candle_stick = CandleStick(USD_JPY, "M5")

    # TODO：private methodに切り出してく
    def run(self):
        print("*** execute process... ***")
        err_count = 0
        while self.status:
            # TODO：いい感じに変える
            if not self.__is_market_open():
                self.__wait_while_market_close()
                continue
            try:
                # TODO：なんかネストがすごいな。。。
                for line in self.candle_stick.streaming_price():
                    if ("bids" in line):  # 価格が更新されてたら

                        if Trader().has_open_positions():
                            print("*** you have open positions ***")
                            # pendingの指値注文があった場合キャンセル
                            if Trader().has_pending_stop_orders():
                                for id in Trader().pending_stop_order_ids():
                                    Trader().cancel_order(id)
                                    print(f"*** canceled order：{id} ***")
                            continue

                        if Trader().has_pending_stop_orders():
                            print("*** you have stop orders ***")
                            continue

                        print(f"*** current price：{line['bids'][0]['price']} ***")

                        # TODO：データ更新の実行はエントリー足の間隔でいい
                        # fixed_candle, avg_candleのデータ更新
                        self.candle_stick.fixed_candle_df()
                        self.candle_stick.avg_candle_df()

                        # エントリー可能な場合、ポジション発注
                        if self.__can_entry():
                            print("*** entry ***")
                            self.__entry()

            except V20Error as e:
                if err_count > 3:
                    self.status = False
                print(e)
                print("*** continue process... ***")
                err_count += 1
        print("*** process end ***")

    # #######
    # private
    # #######

    def __wait_while_market_close(self, sec=300):
        print("market is closed")
        t.sleep(sec)

    def __is_market_open(self):
        market_open = time(7)
        market_close = time(4)
        current_time = datetime.now(timezone(timedelta(hours=+9), 'JST'))
        day_of_week = current_time.today().weekday()
        # 月曜〜土曜の指定期間内
        # TODO：綺麗な条件分けない？
        is_after_open_time = (
            (day_of_week == 0) and (market_open < current_time.time())
        )
        is_before_close_time = (
            (day_of_week == 5) and (current_time.time() < market_close)
        )
        return is_after_open_time or is_before_close_time or (1 <= day_of_week <= 4)

    # strategyの判定実行
    def __can_entry(self):
        return Strategy().is_multi_diversion(self.candle_stick.avg_candles)

    # entry実行
    def __entry(self):
        e_price = Strategy().entry_price(self.candle_stick.avg_candles)
        p_price = Strategy().profit_price(self.candle_stick.avg_candles)
        l_price = Strategy().loss_cut_price(self.candle_stick.avg_candles)

        buy_data = OrderData(USD_JPY, BUY, self.LOT).stop_order(
            str(e_price["buy"]), str(p_price["buy"]), str(l_price["buy"]))
        sell_data = OrderData(USD_JPY, SELL, self.LOT).stop_order(
            str(e_price["sell"]), str(p_price["sell"]), str(l_price["sell"]))

        print(">>> buy_data")
        print(buy_data)
        print(">>> sell_data")
        print(sell_data)

        # 発注
        Trader().order(buy_data)
        Trader().order(sell_data)
