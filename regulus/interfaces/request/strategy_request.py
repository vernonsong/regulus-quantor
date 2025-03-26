# 欲买桂花同载酒，
# 终不似、少年游。
# Copyright (c) VernonSong. All rights reserved.
# ==============================================================================
from datetime import date

from pydantic import BaseModel


class StrategyRequest(BaseModel):
    trade_date: date
