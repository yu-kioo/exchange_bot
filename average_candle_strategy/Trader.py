from oandapyV20 import API
import oandapyV20.endpoints.orders as orders  # 注文の発注
import oandapyV20.endpoints.positions as positions  # 決済・保有中の注文
from oandapyV20.exceptions import V20Error
# user defined
from CommonParams import ACCOUNT_ID, ACCESS_TOKEN, TRADE_ENV

"""
発注・ポジションの確認・決済
"""


class Trader:
    def __init__(self):
        self.client = API(access_token=ACCESS_TOKEN, environment=TRADE_ENV)

    # 発注
    def order(self, data):
        order = orders.OrderCreate(ACCOUNT_ID, data=data)
        self.client.request(order)
        return order.response

    # ポジション
    def has_open_positions(self):
        return True if len(self.__open_positions()["positions"]) > 0 else False

    # 決済
    # TODO：short, longでall, parts別に対応する
    def close_long_positions(self):
        data = {"longUnits": "ALL"}
        order = positions.PositionClose(
            accountID=ACCOUNT_ID, data=data, instrument="USD_JPY")

        self.client.request(order)
        return order.response

    def close_short_positions(self):
        data = {"shortUnits": "ALL"}
        order = positions.PositionClose(
            accountID=ACCOUNT_ID, data=data, instrument="USD_JPY")

        self.client.request(order)
        return order.response

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
