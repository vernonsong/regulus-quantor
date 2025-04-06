# 欲买桂花同载酒，
# 终不似、少年游。
# Copyright (c) VernonSong. All rights reserved.
# ==============================================================================
import base64
from io import BytesIO

import cv2
import numpy as np
import requests
from openai import OpenAI

from regulus.config import ModelConfig


def url_to_image(url: str) -> np.ndarray:
    """
    从给定的URL下载图片并将其转换为OpenCV可以使用的格式。

    :param url: 图片的URL
    :return: OpenCV格式的图像 (numpy数组)
    """
    # 发送HTTP请求获取图片数据
    response = requests.get(url, verify=False)
    response.raise_for_status()  # 检查请求是否成功

    # 将响应内容读取为字节流
    image_data = BytesIO(response.content)

    # 使用OpenCV将字节流解码为图像
    image_array = np.asarray(bytearray(image_data.read()), dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    return image


def resize_image(image: np.ndarray,
                 max_size: int = 5120) -> np.ndarray:
    """
    将 OpenCV 图片按最长边等比例缩放到指定尺寸
    :param image: OpenCV 图片 (BGR 格式)
    :param max_size: 最长边目标尺寸
    :return: 缩放后的图片 (BGR 格式)
    """
    h, w = image.shape[:2]
    scale = max_size / max(h, w)
    new_h, new_w = int(h * scale), int(w * scale)
    return cv2.resize(image, (new_w, new_h),
                      interpolation=cv2.INTER_LANCZOS4)


def image_to_base64(image: np.ndarray, ext: str = '.jpg') -> str:
    """
    将 OpenCV 图片转换为 Base64 字符串
    :param image: OpenCV 图片 (BGR 格式)
    :param ext: 图片扩展名，用于确定编码格式 (支持 .jpg, .png)
    :return: 带 MIME 类型的 Base64 字符串
    """
    # 转换为 RGB 格式避免颜色异常
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 根据扩展名确定编码参数
    ext = ext.lower()
    if ext == '.jpg' or ext == '.jpeg':
        encode_params = [cv2.IMWRITE_JPEG_QUALITY, 95]
    elif ext == '.png':
        encode_params = [cv2.IMWRITE_PNG_COMPRESSION, 5]
    else:
        raise ValueError(f"不支持的图片格式: {ext}")

    # 编码为字节数据
    success, encoded = cv2.imencode(ext, rgb_image, encode_params)
    if not success:
        raise RuntimeError('图片编码失败')
    return base64.b64encode(encoded).decode()


def local_image_to_base64(file_path: str,
                          max_size: int = 5120) -> str:
    """
    读取本地图片 → 缩放 → 转换为 Base64
    :param file_path: 图片路径
    :param max_size: 最长边目标尺寸
    :return: Base64 字符串
    """
    try:

        # 读取图片 (自动转换为 BGR 格式)
        img = cv2.imread(file_path, cv2.IMREAD_COLOR)
        if img is None:
            raise FileNotFoundError(f"无法读取图片文件: {file_path}")

        # 缩放处理
        resized = resize_image(img, max_size)
        return image_to_base64(resized)
    except Exception as e:
        raise RuntimeError(f"本地图片处理失败: {str(e)}")


class ImgRecognizeModel(object):
    """
    图像识别模型
    """

    def __init__(self, model_config: ModelConfig):
        self.client = OpenAI(
            api_key=model_config.api_key,
            base_url=model_config.base_url,
        )

    def __call__(self, img_path: str, prompt: str, *args, **kwargs) -> str:
        img_base64 = local_image_to_base64(img_path)
        base64_url = f'data:image/jpeg;base64,{img_base64}'  # noqa: E231 E702
        completion = self.client.chat.completions.create(
            model='qwen-vl-max-latest',
            messages=[
                {
                    'role':
                    'system',
                    'content': [{
                        'type': 'text',
                        'text': 'You are a helpful assistant.'
                    }],
                },
                {
                    'role':
                    'user',
                    'content': [
                        {
                            'type': 'image_url',
                            'image_url': {
                                'url': base64_url
                            },
                            'min_pixels': 32 * 32 * 4,
                            'max_pixels': 32 * 32 * 10000
                        },
                        {
                            'type': 'text',
                            'text': prompt
                        },
                    ],
                },
            ],
        )

        result = completion.choices[0].message.content
        return result
