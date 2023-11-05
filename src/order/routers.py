from tkinter import EXCEPTION
from typing import List, Self
from asyncpg import Connection
from fastapi import routing
from conn.conn import connect_to_db
from order.db import calculate_cost, create_order, delete_from_products_in_cart_by_user_id, get_products_from_products_in_cart, insert_products_in_products_in_order
from order.models import ProductInCart, ProductOrder

router = routing.APIRouter()


# @router.post("/orders")
# async def create_orders(user_id: int):
#     conn = await connect_to_db()
#     try:
#         prod_in_cart = await get_products_from_products_in_cart(user_id, conn)
#     except Exception as err:
#         print(err)
#     finally:
#         await conn.close()


@router.post("/new_order")
async def new_order_from_cart(user_id: int):
    conn = await connect_to_db()
    try:
        cost=0
        products_in_cart = await get_products_from_products_in_cart(user_id, conn)
        order_id = await create_order(user_id, cost, conn)
        for product in products_in_cart:
            await insert_products_in_products_in_order(ProductOrder(order_id,product.product_id,product.quantity), conn)
        await delete_from_products_in_cart_by_user_id(user_id, conn)
        cost = await calculate_cost(products_in_cart)
    except Exception as er:
        print(er)
    finally:
        await conn.close()