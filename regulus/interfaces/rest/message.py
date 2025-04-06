# 欲买桂花同载酒，
# 终不似、少年游。
# Copyright (c) VernonSong. All rights reserved.
# ==============================================================================
from fastapi import APIRouter, Depends

from regulus.domain.quantor.service import ImgRecognizeService
from regulus.interfaces.dependencies import get_img_recognize_service
from regulus.interfaces.request import ImgRecognizeRequest
from regulus.interfaces.response.img_recognize_reponse import \
    ImgRecognizeResponse

router = APIRouter()


@router.post('/recognize')
def recognize(img_recognize_dto: ImgRecognizeRequest,
              img_recognize_service: ImgRecognizeService = Depends(
                  get_img_recognize_service)):

    result = img_recognize_service.recognize(img_recognize_dto.img_path)
    return ImgRecognizeResponse(type=result.type.value, content=result.content)
