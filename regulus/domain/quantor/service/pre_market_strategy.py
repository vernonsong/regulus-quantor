# 欲买桂花同载酒，
# 终不似、少年游。
# Copyright (c) VernonSong. All rights reserved.
# ==============================================================================
from datetime import date

from regulus.agent.model.deepseek import DeepSeek
from regulus.agent.prompt import load_prompt
from regulus.config import ModelConfig

from ..model import SendPeriod
from ..repository import MessageDailyRepository
from ..repository.stock_price_repository import StockPriceRepository


class PreMarketStrategy:

    def __init__(self, message_daily_repository: MessageDailyRepository,
                 stock_price_daily_repository: StockPriceRepository,
                 model_config: ModelConfig):
        self._message_daily_repository = message_daily_repository
        self._stock_price_daily_repository = stock_price_daily_repository
        self.llm = DeepSeek(api_key=model_config.api_key,
                            api_base=model_config.base_url,
                            model='deepseek-r1',
                            temperature=0.1)

    def generate_strategy(self, trade_date: date):
        message_daily_list = self._message_daily_repository.get_message_list(
            trade_date, SendPeriod.MORNING)
        stock_price_30_day = (self._stock_price_daily_repository.
                              get_stock_price_30_day(trade_date))
        input_prompt = load_prompt('prefix.md') + load_prompt(
            'pre_market_input.md')

        response = self.llm.invoke(
            input_prompt.format(etf_pool=load_prompt('etf_pool.md'),
                                message_from_security_manager='\n'.join([
                                    message_daily.content
                                    for message_daily in message_daily_list
                                ]),
                                etf_score='',
                                after_market_strategy='',
                                trade_date=trade_date,
                                etf_price=str(stock_price_30_day)))

        return response.content
