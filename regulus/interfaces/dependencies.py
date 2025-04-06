# 欲买桂花同载酒，
# 终不似、少年游。
# Copyright (c) VernonSong. All rights reserved.
# ==============================================================================
from fastapi import Depends
from sqlalchemy.orm import Session

from regulus.agent.model import ImgRecognizeModel
from regulus.config import ModelConfig, get_model_config
from regulus.domain.quantor.repository import (MessageDailyRepository,
                                               StockPriceRepository)
from regulus.domain.quantor.service import MessageDailyService
from regulus.domain.quantor.service.img_recognize_service import \
    ImgRecognizeService
from regulus.domain.quantor.service.pre_market_strategy import \
    PreMarketStrategy
from regulus.infrastructure.config import get_db
from regulus.infrastructure.repository import (
    DefaultMessageDailyRepository, DefaultStockPriceDailyRepository)


def get_message_daily_repository(db: Session = Depends(get_db)) -> (
        DefaultMessageDailyRepository):
    return DefaultMessageDailyRepository(db)


def get_stock_price_daily_repository(db: Session = Depends(
        get_db)) -> DefaultStockPriceDailyRepository:
    return DefaultStockPriceDailyRepository(db)


def get_message_daily_service(
        message_daily_repository: MessageDailyRepository = Depends(
            get_message_daily_repository)) -> MessageDailyService:
    return MessageDailyService(message_daily_repository)


def get_pre_market_strategy(
        message_daily_repository: MessageDailyRepository = Depends(
            get_message_daily_service),
        stock_price_repository: StockPriceRepository = Depends(
            get_stock_price_daily_repository),
        model_config: ModelConfig = Depends(get_model_config)
) -> PreMarketStrategy:
    return PreMarketStrategy(message_daily_repository, stock_price_repository,
                             model_config)


def get_img_recognize_model(model_config: ModelConfig = Depends(
        get_model_config)) -> ImgRecognizeModel:
    return ImgRecognizeModel(model_config)


def get_img_recognize_service(img_recognize_model: ImgRecognizeModel = Depends(
        get_img_recognize_model)) -> ImgRecognizeService:
    return ImgRecognizeService(img_recognize_model)
