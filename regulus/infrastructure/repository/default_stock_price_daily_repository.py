# 欲买桂花同载酒，
# 终不似、少年游。
# Copyright (c) VernonSong. All rights reserved.
# ==============================================================================
from datetime import date, timedelta
from typing import List

from sqlalchemy import text
from sqlalchemy.orm import Session

from regulus.domain.quantor.model import StockPriceDaily
from regulus.domain.quantor.repository.stock_price_repository import \
    StockPriceRepository


class DefaultStockPriceDailyRepository(StockPriceRepository):

    def __init__(self, db: Session):
        self.db = db

    def get_stock_price_30_day(self,
                               trade_date: date) -> List[StockPriceDaily]:
        start_date = (trade_date - timedelta(days=30))
        sql = text("""
        SELECT *
        FROM stock_price_daily
        WHERE trade_date >= :start_date
    """)
        result = self.db.execute(sql, {
            'start_date': start_date,
        })

        return [
            StockPriceDaily(stock_code=row.stock_code,
                            trade_date=row.trade_date,
                            open=row.open,
                            close=row.close,
                            high=row.high,
                            low=row.low,
                            volume=row.volume,
                            money=row.money) for row in result
        ]
