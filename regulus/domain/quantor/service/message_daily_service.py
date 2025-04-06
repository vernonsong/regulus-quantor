# 欲买桂花同载酒，
# 终不似、少年游。
# Copyright (c) VernonSong. All rights reserved.
# ==============================================================================
from datetime import datetime
from typing import List

from ..model import SendPeriod
from ..repository import MessageDailyRepository


class MessageDailyService:
    def __init__(self, message_daily_repository: MessageDailyRepository):
        self._message_daily_repository = message_daily_repository

    def get_message_list(self,
                         trade_date: datetime,
                         send_period: SendPeriod) -> List[str]:
        return self._message_daily_repository.get_message_list(trade_date,
                                                               send_period)
