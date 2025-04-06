# 欲买桂花同载酒，
# 终不似、少年游。
# Copyright (c) VernonSong. All rights reserved.
# ==============================================================================
from pathlib import Path
from typing import Any, Dict

import yaml
from fastapi import Depends
from pydantic import BaseModel


def load_yaml_config(file_path: Path) -> Dict[str, Any]:
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)


def deep_merge(base: Dict, update: Dict) -> Dict:
    """递归合并两个字典"""
    for key, value in update.items():
        if isinstance(value, dict):
            node = base.setdefault(key, {})
            deep_merge(node, value)
        else:
            base[key] = value
    return base


class AppConfig(BaseModel):
    name: str
    debug: bool


class DatabaseConfig(BaseModel):
    host: str
    port: int
    dbname: str
    user: str
    password: str


class ModelConfig(BaseModel):
    api_key: str
    base_url: str


class Settings(BaseModel):
    app: AppConfig
    database: DatabaseConfig
    model: ModelConfig

    @classmethod
    def load(cls):
        # 获取配置文件路径
        config_dir = Path(__file__).parent.parent / 'config'

        # 加载基础配置
        base_config = load_yaml_config(config_dir / 'base.yaml')

        # 加载密钥配置
        secret_config = load_yaml_config(config_dir / 'secret.yaml')

        # 合并配置（secret配置优先级更高）
        merged_config = deep_merge(base_config, secret_config)

        # 转换为Pydantic模型
        return cls.model_validate(merged_config)


def get_settings():
    """获取Settings实例作为依赖项"""
    return Settings.load()


def get_model_config(
        settings: Settings = Depends(get_settings)) -> ModelConfig:
    """获取ModelConfig作为依赖项"""
    return settings.model
