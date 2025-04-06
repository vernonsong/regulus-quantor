# 欲买桂花同载酒，
# 终不似、少年游。
# Copyright (c) VernonSong. All rights reserved.
# ==============================================================================
from abc import ABC, abstractmethod
from datetime import date
from typing import List

from regulus.domain.quantor.model import MessageDaily, SendPeriod


class MessageDailyRepository(ABC):

    @abstractmethod
    def get_message_list(self, trade_date: date,
                         send_period: SendPeriod) -> List[MessageDaily]:
        pass
