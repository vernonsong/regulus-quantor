# 欲买桂花同载酒，
# 终不似、少年游。
# Copyright (c) VernonSong. All rights reserved.
# ==============================================================================
from abc import ABC, abstractmethod
from datetime import date
from typing import List

from regulus.domain.quantor.model import PreMarketInfo, StockPriceDaily


class MarketInfoRepository(ABC):
    """
    市场信息 仓储层抽象
    """

    @abstractmethod
    def get_pre_market_info(self, trade_date: date) -> PreMarketInfo:
        """
        获取盘前策略所需市场信息
        :param trade_date: 交易日期
        :return: PreMarketInfo
        """
        pass

    @abstractmethod
    def get_stock_price_30_day(self, trade_date: date) -> List[StockPriceDaily]:
        """
        获取近30天行情数据
        :param trade_date: 交易日期
        :return: List[StockPriceDaily]
        """
        pass
