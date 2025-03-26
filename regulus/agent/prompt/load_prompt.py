# 欲买桂花同载酒，
# 终不似、少年游。
# Copyright (c) VernonSong. All rights reserved.
# ==============================================================================
from pathlib import Path


def load_prompt(file_name: str) -> str:
    """
    读取与当前方法所在目录相同的文件。

    :param file_name: 要读取的文件名
    :return: 文件的内容
    """
    # 获取当前脚本所在的目录
    current_dir = Path(__file__).parent

    # 构建文件的完整路径
    file_path = current_dir / file_name

    # 检查文件是否存在
    if not file_path.exists():
        raise FileNotFoundError(f"文件 {file_path} 不存在")

    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    return content
