# 欲买桂花同载酒，
# 终不似、少年游。
# Copyright (c) VernonSong. All rights reserved.
# ==============================================================================
from datetime import date
from typing import List

from sqlalchemy import text
from sqlalchemy.orm import Session

from regulus.domain.quantor.model import MessageDaily, SendPeriod
from regulus.domain.quantor.repository import MessageDailyRepository


class DefaultMessageDailyRepository(MessageDailyRepository):

    def __init__(self, db: Session):
        self.db = db

    def get_message_list(self, trade_date: date,
                         send_period: SendPeriod) -> List[MessageDaily]:
        sql = text("""
               SELECT content, source, trade_date, send_period
               FROM message_daily
               WHERE trade_date = :trade_date
               AND send_period = :send_period
           """)

        # 执行参数化查询
        result = self.db.execute(sql, {
            'trade_date': trade_date,
            'send_period': send_period.name
        })

        # 将结果映射为 MessageDaily 对象列表
        return [
            MessageDaily(
                content=row.content,
                source=row.source,
                trade_date=row.trade_date,
                send_period=SendPeriod(row.send_period)  # 将字符串转换为枚举类型
            ) for row in result
        ]
