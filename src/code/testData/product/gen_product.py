# -*- coding: utf-8 -*-
import random
from faker import Faker

fake = Faker()

# 预定义商品类别
categories = [
    "electronics",
    "home_kitchen",
    "clothing",
    "sports_outdoors",
    "beauty",
    "books",
    "toys_games",
    "automotive",
    "health",
    "grocery",
]


# 生成商品名称和描述的函数
def generate_product_name(category):
    if category == "electronics":
        return f"{fake.word().capitalize()} Smart {random.choice(['Phone', 'Watch', 'Speaker', 'Camera'])}"
    elif category == "home_kitchen":
        return f"{fake.word().capitalize()} {random.choice(['Blender', 'Toaster', 'Cookware Set', 'Air Fryer'])}"
    elif category == "clothing":
        return (
            f"{fake.word().capitalize()} {random.choice(['T-Shirt', 'Jeans', 'Jacket', 'Dress'])}"
        )
    elif category == "sports_outdoors":
        return f"{fake.word().capitalize()} {random.choice(['Running Shoes', 'Yoga Mat', 'Tent', 'Bicycle'])}"
    elif category == "beauty":
        return f"{fake.word().capitalize()} {random.choice(['Lipstick', 'Perfume', 'Moisturizer', 'Face Mask'])}"
    elif category == "books":
        return f"Book: {fake.catch_phrase()}"
    elif category == "toys_games":
        return f"{fake.word().capitalize()} {random.choice(['LEGO Set', 'Board Game', 'Action Figure', 'Puzzle'])}"
    elif category == "automotive":
        return f"{fake.word().capitalize()} {random.choice(['Car Wax', 'Tire Pump', 'Seat Cover', 'Jump Starter'])}"
    elif category == "health":
        return f"{fake.word().capitalize()} {random.choice(['Vitamin', 'Protein Powder', 'First Aid Kit', 'Massager'])}"
    elif category == "grocery":
        return f"{fake.word().capitalize()} {random.choice(['Coffee', 'Snack Bar', 'Pasta', 'Olive Oil'])}"


def generate_product_description(name):
    return f"High-quality {name.lower()}. Perfect for everyday use."

def generate_product_data():
    # 生成 1000 条数据
    data = []
    for i in range(1, 1001):
        category = random.choice(categories)
        name = generate_product_name(category)
        description = generate_product_description(name)
        price = round(random.uniform(10.0, 1000.0), 2)
        stock = random.randint(0, 500)
        status = random.choice(["active", "inactive"])
        rating = round(random.uniform(0.0, 5.0), 2)

        data.append((name, description, price, category, stock, status, rating))

    # 输出 SQL 插入语句
    sql_statements = []
    for product in data:
        sql = f"""
        INSERT INTO products (name, description, price, category, stock, status, rating)
        VALUES ('{product[0]}', '{product[1]}', {product[2]}, '{product[3]}', {product[4]}, '{product[5]}', {product[6]});
        """
        sql_statements.append(sql)

    with open("product.sql", "w") as file:
        for sql in sql_statements:
            # 写入每条 SQL 语句，并在其后添加换行符
            file.write(sql + "\n")
            
    return data
