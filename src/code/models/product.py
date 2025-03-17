# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP, Enum, text, Index
from db.database import Base
from pydantic import BaseModel


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    price = Column(DECIMAL(10, 2), nullable=False)
    category = Column(String(100), nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )
    status = Column(Enum("active", "inactive"), nullable=False, default="active")
    rating = Column(DECIMAL(3, 2))


# 定义二级索引
Index("idx_category_price", Product.category, Product.price)  # 按分类和价格查询
Index("idx_status_created_at", Product.status, Product.created_at)  # 按状态和创建时间查询
Index("idx_name", Product.name)  # 按商品名称模糊搜索


# 修改库存（原子操作）
class StockUpdate(BaseModel):
    delta: int  # 库存变化量（可正可负）