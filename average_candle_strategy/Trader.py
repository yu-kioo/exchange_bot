import json
from oandapyV20 import API
import oandapyV20.endpoints.orders as orders  # 注文の発注
import oandapyV20.endpoints.positions as positions  # 決済・保有中の注文
from oandapyV20.exceptions import V20Error
# user defined
from average_candle_strategy.CommonParams import ACCOUNT_ID, ACCESS_TOKEN, TRADE_ENV

"""
発注・ポジションの確認・決済
"""


class Trader:
    LIMIT = "LIMIT"

    def __init__(self):
        self.client = API(access_token=ACCESS_TOKEN, environment=TRADE_ENV)

    # 発注
    def order(self, data):
        print(">>> Trader::order")
        order = orders.OrderCreate(ACCOUNT_ID, data=data)
        self.client.request(order)
        print(">>> response")
        print(order.response)

    def has_open_positions(self):
        return len(self.__open_positions()["positions"]) > 0

    def has_pending_orders(self):
        return not (len(self.pending_order_ids()) == 0)

    def has_pending_limit_orders(self):
        return not (len(self.pending_limit_order_ids()) == 0)

    # 未成約注文
    def pending_order_ids(self):
        req = orders.OrdersPending(ACCOUNT_ID)
        self.client.request(req)
        result = [x["id"] for x in req.response["orders"]]
        return result

    # 未成約指値注文
    def pending_limit_order_ids(self):
        req = orders.OrdersPending(ACCOUNT_ID)
        self.client.request(req)
        result = [
            x["id"]for x in req.response["orders"] if x["type"] == self.LIMIT
        ]
        return result

    # 決済
    def close_long_positions(self):
        # TODO：position存在を確認するガード節いれる
        data = {"longUnits": "ALL"}
        order = positions.PositionClose(
            accountID=ACCOUNT_ID, data=data, instrument="USD_JPY")

        self.client.request(order)
        return order.response

    def close_short_positions(self):
        # TODO：position存在を確認するガード節いれる
        data = {"shortUnits": "ALL"}
        order = positions.PositionClose(
            accountID=ACCOUNT_ID, data=data, instrument="USD_JPY")

        self.client.request(order)
        return order.response

    # オーダーキャンセル
    # TODO:idsを使ってfor文内部で使用することをManagerが知ってるので隠蔽する
    def cancel_order(self, id):
        req = orders.OrderCancel(ACCOUNT_ID, orderID=id)
        self.client.request(req)
        print(">>> cancel order")
        print(f">>> {req.response}")
        return req.response

    # トレイリング
    def trailing(self):
        return None

    # #######
    # private
    # #######

    def __open_positions(self):
        p = positions.OpenPositions(accountID=ACCOUNT_ID)
        self.client.request(p)
        return p.response
