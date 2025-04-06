# 欲买桂花同载酒，
# 终不似、少年游。
# Copyright (c) VernonSong. All rights reserved.
# ==============================================================================
from fastapi import APIRouter, Depends

from regulus.domain.quantor.service.pre_market_strategy import \
    PreMarketStrategy
from regulus.interfaces.dependencies import get_pre_market_strategy
from regulus.interfaces.request import StrategyRequest
from regulus.interfaces.response import StrategyResponse

router = APIRouter()


@router.post('/pre_market_strategy')
def get_user(strategy_request: StrategyRequest,
             pre_market_strategy: PreMarketStrategy = Depends(
                 get_pre_market_strategy)):
    content = pre_market_strategy.generate_strategy(
        strategy_request.trade_date)
    return StrategyResponse(content=content)
