# 欲买桂花同载酒，
# 终不似、少年游。
# Copyright (c) VernonSong. All rights reserved.
# ==============================================================================
from fastapi import Depends
from sqlalchemy.orm import Session

from regulus.agent.model import ImgRecognizeModel
from regulus.config import ModelConfig, get_model_config
from regulus.domain.quantor.repository import MarketInfoRepository
from regulus.domain.quantor.service.img_recognize_service import \
    ImgRecognizeService
from regulus.domain.quantor.service.pre_market_strategy import \
    PreMarketStrategy
from regulus.infrastructure.config import get_db
from regulus.infrastructure.repository import DefaultMarketInfoRepository


def get_market_info_repository(db: Session = Depends(get_db)) -> (
        MarketInfoRepository):
    return DefaultMarketInfoRepository(db)


def get_pre_market_strategy(
        market_info_repository: MarketInfoRepository = Depends(
                get_market_info_repository),
        model_config: ModelConfig = Depends(get_model_config)
) -> PreMarketStrategy:
    return PreMarketStrategy(market_info_repository, model_config)


def get_img_recognize_model(model_config: ModelConfig = Depends(
        get_model_config)) -> ImgRecognizeModel:
    return ImgRecognizeModel(model_config)


def get_img_recognize_service(img_recognize_model: ImgRecognizeModel = Depends(
        get_img_recognize_model)) -> ImgRecognizeService:
    return ImgRecognizeService(img_recognize_model)
