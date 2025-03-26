# 欲买桂花同载酒，
# 终不似、少年游。
# Copyright (c) VernonSong. All rights reserved.
# ==============================================================================
from datetime import date

from pydantic import BaseModel


class StockPriceDaily(BaseModel):
    stock_code: str
    trade_date: date
    open: float
    close: float
    high: float
    low: float
    volume: float
    money: float
