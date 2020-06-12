import json
# user defined
from average_candle_strategy.CommonParams import BUY, SELL, ORDER_TYPE


"""
オーダーのデータクラス
"""


class OrderData:
    def __init__(self, instrument, kind, lot):
        self.data = {"order": {}}
        self.kind = kind
        self.lot = lot

        self.data["order"]["instrument"] = instrument
        self.data["order"]["units"] = self.lot if self.kind == "BUY" else -self.lot

    # 成り行き注文
    def market_order(self):
        self.data["order"]["type"] = ORDER_TYPE["MARKET"]
        return self.data

    # 逆指値注文
    def stop_order(self, limit_price, profit_price, loss_price):
        self.data["order"]["type"] = ORDER_TYPE["STOP"]
        self.data["order"]["price"] = limit_price
        self.data["order"]["takeProfitOnFill"] = {"price": profit_price}
        self.data["order"]["stopLossOnFill"] = {"price": loss_price}
        return self.data
