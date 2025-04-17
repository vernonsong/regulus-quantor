# 欲买桂花同载酒，
# 终不似、少年游。
# Copyright (c) VernonSong. All rights reserved.
# ==============================================================================
from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class MessageDaily(BaseModel):
    content: Optional[str] = None
    source: str


class PreMarketInfo(BaseModel):
    analyze_content: List[MessageDaily]
    position: Optional[str] = None
    strategy_score: Optional[str] = None
    trade_date: date
