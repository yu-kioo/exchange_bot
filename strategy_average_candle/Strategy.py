import pandas as pd
import json
import oandapyV20.endpoints.orders as orders  # 注文の発注
import oandapyV20.endpoints.positions as positions  # 決済・保有中の注文
from oandapyV20 import API
from oandapyV20.exceptions import V20Error
# user defined
from CommonParams import ACCESS_TOKEN, TRADE_ENV, TRADE_ENV

"""
売買の可否を判断する
"""


class Strategy:

    # TODO：x_range(判定するロウソク足の本数)をクラス変数化する
    ENTITY_RANGE = 0.006  # 実体の制限値幅
    PERCENT_RANGE = 19  # ロウソク足に対する実体の比率(%)
    ENTRY_RANGE = 0.08  # エントリーに指定する高安値に加える緩衝値

    def __init__(self):
        self.client = API(access_token=ACCESS_TOKEN, environment=TRADE_ENV)

    # 指定した範囲の中で転換足が一定数出現したか
    # count = 転換足の本数 , x_range = ロウソク本数の範囲 , y_range = 値幅
    def is_multi_diversion(self, avg_candle_df, count=2, x_range=4, y_range=0.04):

        # 最新からx_range範囲に転換足があるか
        # TODO：ここの処理汚くね。。？
        flags = [self.__is_diversion_candle(
            avg_candle_df.iloc[-i]) for i in range(1, x_range + 1)]
        if (len(list(filter(lambda x: x == True, flags))) >= 2):
            return True
        else:
            return False

    # エントリーラインを定める
    def entry_price(self, avg_candle_df, x_range=4):
        ids = self.__diversion_ids(avg_candle_df)

        high = [avg_candle_df.iloc[i].high for i in ids]
        low = [avg_candle_df.iloc[i].low for i in ids]

        return {"high": max(high) + self.ENTRY_RANGE, "low": min(low) - self.ENTRY_RANGE}

    # 利確ラインを定める
    def target_price(self, avg_candle_df):
        price = self.entry_price(avg_candle_df)

        # 一旦固定5pipsにする
        # TODO：エントリー足に合わせて利確幅を調節する
        return {"high": price["high"] + 0.05, "low": price["low"] - 0.05}

    # 損切りラインを定める
    def loss_cut_price(self, avg_candle_df):
        #

        return None

    # #######
    # private
    # #######

    # 単体の足が転換足かの判定
    def __is_diversion_candle(self, row):
        if pd.isnull(row.open):
            return False

        overall = round(abs(row.high - row.low), 3)  # ロウソク足全体(高安値)の値幅
        entity = round(abs(row.open - row.close), 3)  # 実体の値幅

        # 小陽陰線かどうか
        # TODO：より幅のある綺麗な線の方が勝率高そうだったら差分に値幅を設ける
        is_candle_with_beard = (
            True if (
                (row.low < row.open < row.close < row.high) or (
                    row.low < row.close < row.open < row.high)
            ) else False
        )
        # 実体が一定値以下、もしくは実体の比率が指定値以下 かつ 小陽陰線(始値・終値が高値・安値よりも小さい)
        return ((entity < self.ENTITY_RANGE) or ((overall / entity) * 100 < self.PERCENT_RANGE)) and is_candle_with_beard

    # 転換足のid
    def __diversion_ids(self, avg_candle_df, x_range=4):
        # TODO:リスト内包にif加えれば簡略化出来そう
        result = []
        for index, row in avg_candle_df[len(avg_candle_df) - x_range: len(avg_candle_df)].iterrows():
            # noneの場合の処理飛ばす
            if self.__is_diversion_candle(row):
                result.append(index)

        return result
