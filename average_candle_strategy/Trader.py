import json
import oandapyV20.endpoints.orders as orders  # 注文の発注
import oandapyV20.endpoints.positions as positions  # 決済・保有中の注文
# user defined
from average_candle_strategy.CommonParams import ACCOUNT_ID, ORDER_TYPE
from average_candle_strategy.oandaAPI.TradeAPI import TradeAPI

"""
発注・ポジションの確認・決済
"""


class Trader:
    # 発注
    def order(self, data):
        print(">>> Trader::order")
        res = TradeAPI().order(data)
        print(">>> response")
        print(res)

    def has_open_positions(self):
        return len(self.__open_positions()["positions"]) > 0

    def has_pending_orders(self):
        return not (len(self.pending_order_ids()) == 0)

    def has_pending_limit_orders(self):
        return not (len(self.pending_limit_order_ids()) == 0)

    # 未成約注文
    def pending_order_ids(self):
        res = TradeAPI().pending_orders()
        result = [x["id"] for x in res["orders"]]
        return result

    # 未成約指値注文
    def pending_limit_order_ids(self):
        res = TradeAPI().pending_orders()
        result = [
            x["id"]for x in res["orders"] if x["type"] == ORDER_TYPE["LIMIT"]
        ]
        return result

    # 決済
    def close_long_positions(self, instrument):
        return TradeAPI().close_long_positions(instrument)

    def close_short_positions(self, instrument):
        return TradeAPI().close_short_positions(instrument)

    # オーダーキャンセル
    # TODO:idsを使ってfor文内部で使用することをManagerが知ってるので隠蔽する
    def cancel_order(self, id):
        print(">>> cancel order")
        res = TradeAPI().cancel_order(id)
        print(f">>> {res}")
        return res

    # トレイリング
    def trailing(self):
        return None

    # #######
    # private
    # #######

    def __open_positions(self):
        return TradeAPI().open_positions()
