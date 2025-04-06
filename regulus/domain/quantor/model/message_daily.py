# 欲买桂花同载酒，
# 终不似、少年游。
# Copyright (c) VernonSong. All rights reserved.
# ==============================================================================
from datetime import date
from typing import Optional

from pydantic import BaseModel

from .send_period import SendPeriod


class MessageDaily(BaseModel):
    content: Optional[str] = None
    source: str
    trade_date: date
    send_period: SendPeriod
