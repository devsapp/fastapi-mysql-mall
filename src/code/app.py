# -*- coding: utf-8 -*-

from fastapi import FastAPI, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from models.product import Product, StockUpdate
from typing import Optional
from db.database import engine, get_db, Base, SessionLocal
import time
from db.cache import defaultCache
import os
from fastapi import Form, Request
from fastapi.responses import RedirectResponse
import requests
from testData.product.gen_product import generate_product_data
from fastapi.templating import Jinja2Templates


# 创建一个会话对象
session = requests.Session()
templates = Jinja2Templates(directory="templates")

app = FastAPI()

# 新增：在应用启动时创建表
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    # 检查是否需要插入数据
    db = SessionLocal()
    try:
        # 检查 products 表是否为空
        if db.query(Product).first() is None:
            print("Products table is empty. Inserting initial data.")
            product_data = generate_product_data()
            for product in product_data:
                new_product = Product(
                    name=product[0],
                    description=product[1],
                    price=product[2],
                    category=product[3],
                    stock=product[4],
                    status=product[5],
                    rating=product[6]
                )
                db.add(new_product)
            db.commit()
            print(f"Generated and inserted {len(product_data)} products")
        else:
            print("Products table already contains data. Skipping data insertion.")
    except Exception as e:
        db.rollback()
        print(f"Error during database operation: {e}")
    finally:
        db.close()


@app.on_event("shutdown")
async def shutdown_event():
    session.close()


# 中间件
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Process-Region"] = os.environ.get("FC_REGION", "unknown")
    return response


# 查询商品（按商品ID, 1-1000）
@app.get("/products/{product_id}")
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    cache_key = f"product_{product_id}"
    result = defaultCache.get(cache_key)
    if result is not None:
        print(f"get_product_by_id: Cache hit for product {product_id}")
        return result

    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    result = {
        "product_id": product.product_id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "category": product.category,
        "stock": product.stock,
        "created_at": product.created_at,
        "updated_at": product.updated_at,
        "status": product.status,
        "rating": product.rating,
    }
    defaultCache.set(
        cache_key,
        result,
        ttl=1,
    )
    return result

# 查询商品（按分类、 价格升降序）
@app.get("/products")
def get_products(
    name: str,
    category: Optional[str] = Query(None),
    price_asc: Optional[bool] = Query(True),
    db: Session = Depends(get_db),
):
    if category:
        # 如果提供了category，根据category查询数据库
        products = (
            db.query(Product)
            .filter(Product.category == category, Product.name.like(f"%{name}%"))
            .order_by(Product.price.asc() if price_asc else Product.price.desc())
            .limit(10)
            .all()
        )
    else:
        # 如果没有提供category，返回所有产品
        products = (
            db.query(Product)
            .order_by(Product.price.asc() if price_asc else Product.price.desc())
            .limit(10)
            .all()
        )

    return products

@app.patch("/products/{product_id}/stock")
def update_stock(product_id: int, stock_update: StockUpdate, db: Session = Depends(get_db)):
    # 原子操作更新库存，防止超卖
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    new_stock = product.stock + stock_update.delta
    if new_stock < 0:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    product.stock = new_stock
    db.commit()
    return {
        "message": f"'{product.name}' stock updated",
        "product_id": product_id,
        "new_stock": new_stock,
    }

@app.post("/admin/products/{product_id}/set_stock", include_in_schema=False)
def admin_set_stock(
    product_id: int,
    new_stock: int = Form(...),
    page: int = Query(1),
    size: int = Query(10),
    db: Session = Depends(get_db),
):
    if new_stock < 0:
        raise HTTPException(status_code=400, detail="Stock cannot be negative")
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.stock = new_stock
    db.commit()
    # 清除缓存
    cache_key = f"product_{product_id}"
    defaultCache.delete(cache_key)
    return RedirectResponse(
        url=f"/?page={page}&size={size}",
        status_code=303,
    )
    
@app.get("/", include_in_schema=False)
def admin_page(
    request: Request,
    search_id: Optional[int] = Query(None, alias="search"),  # 新增搜索参数
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    # 搜索逻辑
    if search_id:
        product = db.query(Product).filter(Product.product_id == search_id).first()
        products = [product] if product else []
        total = 1 if product else 0
        total_pages = 1
    else:
        # 原有分页逻辑
        offset = (page - 1) * size
        products = (
            db.query(Product)
            .order_by(Product.created_at.desc())
            .offset(offset)
            .limit(size)
            .all()
        )
        total = db.query(Product).count()
        total_pages = (total + size - 1) // size

    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "products": products,
            "page": page,
            "size": size,
            "total_pages": total_pages,
            "search_id": search_id,  # 传递搜索参数到模板
        },
    )

@app.post("/initialize", include_in_schema=False)
def initialize(db: Session = Depends(get_db)):
    db.query(Product).filter(Product.product_id == 1).first()
    print("initialize success")
    return {"status": "success"}
