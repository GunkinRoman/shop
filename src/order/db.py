from asyncpg import Connection
from typing import List
from conn.conn import connect_to_db
from order.models import ProductOrder, ProductInCart


async def get_products_from_products_in_cart(user_id: int, conn: Connection) -> List[ProductInCart]:
    query = "SELECT * FROM product_in_cart WHERE acc_id = $1"
    rows = await conn.fetch(query, user_id)
    products = []
    for row in rows:
        product = ProductInCart(row['id'], row['acc_id'], row['product'], row['quantity'])
        products.append(product)
    return products

async def create_order(user_id: int, cost: float, conn: Connection) -> int:
    query = "INSERT INTO orders (acc_id, cost, paid) VALUES ($1, $2, $3) returning id"
    return int(await conn.fetchval(query, user_id, cost, False)) # type: ignore

async def insert_products_in_products_in_order(products: ProductOrder, conn: Connection) -> None:
    query = "INSERT INTO products_order (order_id, product, quantity) VALUES ($1, $2, $3)"
    await conn.execute(query, products.order_id, products.product_id, products.quantity)

async def delete_from_products_in_cart_by_user_id(user_id: int, conn: Connection) -> None:
    query = "DELETE FROM product_in_cart WHERE acc_id = $1"
    await conn.execute(query, user_id)

async def calculate_cost(products_in_cart: List[ProductInCart]) -> float:
    cost = 0
    for product in products_in_cart:
        query = "SELECT cost FROM product WHERE id = $1"
        row = await connect_to_db.fetchrow(query, product.product_id)
        cost += row['cost'] * product.quantity
    return cost
