from oandapyV20 import API
from oandapyV20.exceptions import V20Error
from average_candle_strategy.CommonParams import ACCESS_TOKEN, TRADE_ENV


class Base(object):
    def __init__(self):
        self.client = API(access_token=ACCESS_TOKEN, environment=TRADE_ENV)
