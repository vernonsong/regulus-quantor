# 欲买桂花同载酒，
# 终不似、少年游。
# Copyright (c) VernonSong. All rights reserved.
# ==============================================================================
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from regulus.config.setting import Settings

settings = Settings.load()


# 构建MySQL连接URL
DATABASE_URL = (
    f"mysql+pymysql://"  # noqa: E231
    f"{settings.database.user}:"  # noqa: E231
    f"{settings.database.password}"
    f"@{settings.database.host}:"  # noqa: E231
    f"{settings.database.port}/"
    f"{settings.database.dbname}"
    '?charset=utf8mb4'
)
# 核心配置
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    pool_pre_ping=True,
    pool_recycle=3600
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# FastAPI 依赖注入
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
