# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DB')}"

# 创建引擎并配置连接池
engine = create_engine(
    DATABASE_URL,
    pool_size=10,  # 连接池保持的连接数
    max_overflow=20,  # 连接池最大溢出连接数
    pool_pre_ping=True,  # 执行前检查连接有效性
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# 数据库依赖注入
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
