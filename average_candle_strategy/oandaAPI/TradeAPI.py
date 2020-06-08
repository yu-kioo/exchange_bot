import oandapyV20.endpoints.orders as orders  # 注文の発注
import oandapyV20.endpoints.positions as positions  # 決済・保有中の注文
from oandapyV20.exceptions import V20Error
# user defined
from average_candle_strategy.oandaAPI.Base import Base
from average_candle_strategy.CommonParams import ACCOUNT_ID


class TradeAPI(Base):
    def __init__(self):
        super().__init__()

    # __open_positions
    def order(self, req_data):
        req = orders.OrderCreate(ACCOUNT_ID, data=req_data)
        self.__request(req)
        return req.response

    def pending_orders(self):
        req = orders.OrdersPending(ACCOUNT_ID)
        self.__request(req)
        return req.response

    def close_long_positions(self, instrument):
        # TODO：position存在を確認するガード節いれる
        req = positions.PositionClose(
            accountID=ACCOUNT_ID, data={"longUnits": "ALL"}, instrument=instrument)
        self.__request(req)
        return req.response

    def close_short_positions(self, instrument):
        # TODO：position存在を確認するガード節いれる
        req = positions.PositionClose(
            accountID=ACCOUNT_ID, data={"shortUnits": "ALL"}, instrument=instrument)
        self.__request(req)
        return req.response

    def cancel_order(self, id):
        req = orders.OrderCancel(ACCOUNT_ID, orderID=id)
        self.__request(req)
        return req.response

    def open_positions(self):
        req = positions.OpenPositions(accountID=ACCOUNT_ID)
        self.__request(req)
        return req.response

        # #######
        # private
        # #######

    def __request(self, req_obj):
        return self.client.request(req_obj)
