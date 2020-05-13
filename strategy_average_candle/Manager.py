"""
他のクラスをまとめて一連の処理を組み立てる
"""


class Manager:

    # 価格の取得・エントリー判定・エントリー・決済まで一連のrun実行するまとめ関数
    def execute_process(self):

        while True:
            # 価格取得(generator_obj)
            data = get_current_price()
            for line in data:
                if ("bids" in line)  # 価格が更新されてたら
                execute_strategy(price['bids'][0]['price'], candle_df)

            return None

            # エントリー判定・実行・決済
    def run(self):
        return None

        # エントリー判定のストラテジー

    def execute_strategy(self):
        return None

        # エントリー関係のやつ(ここ１つにするのか微妙なとこ)
    def entry(self):
        return None
