import os
import pathlib
from dotenv import load_dotenv, find_dotenv

"""
共通の定数・環境変数
"""

load_dotenv(find_dotenv())

# TODO：class化する？意味はある？

ACCOUNT_ID = os.getenv("ACCOUNT_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
TRADE_ENV = os.getenv("TRADE_ENV")

USD_JPY = "USD_JPY"

BUY = "BUY"
SELL = "SELL"

# 注文タイプ
ORDER_TYPE = {
    "MARKET": "MARKET",  # 成行
    "LIMIT": "LIMIT",  # 指値
    "STOP": "STOP",  # 逆指値
    "MARKET_IF_TOUCHED": "MARKET_IF_TOUCHED",  # イフタッチ
    "TAKE_PROFIT": "TAKE_PROFIT",  # 利益確定
    "STOP_LOSS": "STOP_LOSS",  # 損失確定
    "TRAILING_STOP_LOSS": "TRAILING_STOP_LOSS",  # トレイリング
}
