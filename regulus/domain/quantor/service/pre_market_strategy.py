# 欲买桂花同载酒，
# 终不似、少年游。
# Copyright (c) VernonSong. All rights reserved.
# ==============================================================================
from datetime import date

from regulus.agent.model.deepseek import DeepSeek
from regulus.agent.prompt import load_prompt
from regulus.config import ModelConfig
from regulus.domain.quantor.repository import MarketInfoRepository


class PreMarketStrategy:
    """
    盘前策略
    """

    def __init__(self, market_info_reposition: MarketInfoRepository,
                 model_config: ModelConfig):
        """
        构造函数
        :param market_info_reposition: 市场信息仓储层
        :param model_config: 模型配置
        """
        self._market_info_reposition = market_info_reposition
        self.llm = DeepSeek(api_key=model_config.api_key,
                            api_base=model_config.base_url, model='deepseek-r1',
                            temperature=0.1)

    def generate_strategy(self, trade_date: date) -> str:
        """
        生成盘前策略
        :param trade_date: 交易日期
        :return: 策略内容
        """
        pre_market_info = self._market_info_reposition.get_pre_market_info(
                trade_date)
        stock_price_30_day = (
                self._market_info_reposition.get_stock_price_30_day(trade_date))
        input_prompt = load_prompt('prefix.md') + load_prompt(
                'pre_market_input.md')

        response = self.llm.invoke(
                input_prompt.format(
                        etf_pool=load_prompt('etf_pool.md'),
                        message_from_security_manager='\n'.join([
                                analyze_content.content for analyze_content in
                                pre_market_info.analyze_content
                        ]), etf_score='', after_market_strategy='',
                        position=pre_market_info.position
                        if pre_market_info.position is not None else '空仓',
                        trade_date=trade_date,
                        etf_price=str(stock_price_30_day)))

        return response.content
