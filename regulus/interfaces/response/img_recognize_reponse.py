# 欲买桂花同载酒，
# 终不似、少年游。
# Copyright (c) VernonSong. All rights reserved.
# ==============================================================================
from pydantic import BaseModel


class ImgRecognizeResponse(BaseModel):
    type: str
    content: str
