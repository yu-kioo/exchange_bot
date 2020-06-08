
import oandapyV20.endpoints.instruments as instruments  # candle情報の取得
from oandapyV20.endpoints.pricing import PricingInfo  # 現在価格の取得
from oandapyV20.endpoints.pricing import PricingStream  # 現在価格のgenerator_obj
from oandapyV20.exceptions import V20Error
# user defined
from average_candle_strategy.CommonParams import ACCOUNT_ID
from average_candle_strategy.oandaAPI.Base import Base


class CandleStickAPI(Base):
    def __init__(self):
        super().__init__()

    def streaming_price(self, instrument):
        req = PricingStream(accountID=ACCOUNT_ID, params={
            "instruments": instrument})
        return self.__request(req)

    def fixed_candle_data(self, instrument, params):
        req = instruments.InstrumentsCandles(
            instrument=instrument, params=params)

        try:
            self.__request(req)
        except V20Error as e:
            print("Error: {}".format(e))

        return req.response

    # #######
    # private
    # #######

    def __request(self, req_obj):
        return self.client.request(req_obj)
