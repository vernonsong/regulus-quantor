# 欲买桂花同载酒，
# 终不似、少年游。
# Copyright (c) VernonSong. All rights reserved.
# ==============================================================================
from enum import Enum


class ImgType(Enum):
    """
    图片类型枚举
    ANALYZE: 研报分析类型
    POSITION: 持仓截图类型
    """
    ANALYZE = 'analyze'
    POSITION = 'position'
