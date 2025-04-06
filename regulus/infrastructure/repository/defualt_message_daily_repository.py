# 欲买桂花同载酒，
# 终不似、少年游。
# Copyright (c) VernonSong. All rights reserved.
# ==============================================================================
from datetime import date, timedelta
from typing import List

from sqlalchemy import text
from sqlalchemy.orm import Session

from regulus.domain.quantor.model import (MessageDaily, PreMarketInfo,
                                          SendPeriod, StockPriceDaily)
from regulus.domain.quantor.repository import MarketInfoRepository


class DefaultMarketInfoRepository(MarketInfoRepository):

    def __init__(self, db: Session):
        self.db = db

    def get_pre_market_info(self, trade_date: date) -> PreMarketInfo:
        # 使用参数化查询防止SQL注入，并复用数据库连接
        # 查询早间消息内容
        message_query = text("""
            SELECT content, source
            FROM message_daily
            WHERE trade_date = :trade_date
              AND send_period = :send_period
        """)

        # 查询前一日仓位（修正拼写错误position）
        position_query = text("""
            SELECT position
            FROM position_daily
            WHERE trade_date = :previous_date
        """)

        # 使用明确的参数命名
        params = {
                'trade_date': trade_date,
                'send_period': SendPeriod.MORNING.value,
                'previous_date': trade_date - timedelta(days=1)
        }

        with self.db.begin():
            # 通过 session.connection() 获取实际的数据库连接
            connection = self.db.connection()
            # 执行第一个查询并立即获取结果
            message_records = connection.execute(
                    message_query, {
                            'trade_date': params['trade_date'],
                            'send_period': params['send_period']
                    }).fetchall()

            # 执行第二个查询并立即获取结果
            position_records = connection.execute(
                    position_query, {
                            'previous_date': params['previous_date']
                    }).fetchall()

        # 构造结果对象
        return PreMarketInfo(
                analyze_content=[
                        MessageDaily(content=row.content, source=row.source)
                        for row in message_records
                ], position=position_records[0].position
                if position_records else None, trade_date=trade_date)

    def get_stock_price_30_day(self, trade_date: date) -> List[StockPriceDaily]:
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
                                trade_date=row.trade_date, open=row.open,
                                close=row.close, high=row.high, low=row.low,
                                volume=row.volume, money=row.money)
                for row in result
        ]
