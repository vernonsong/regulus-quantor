# 欲买桂花同载酒，
# 终不似、少年游。
# Copyright (c) VernonSong. All rights reserved.
# ==============================================================================
from abc import ABC, abstractmethod
from datetime import date
from typing import List

from regulus.domain.quantor.model import StockPriceDaily


class StockPriceRepository(ABC):

    @abstractmethod
    def get_stock_price_30_day(self,
                               trade_date: date) -> List[StockPriceDaily]:
        pass
