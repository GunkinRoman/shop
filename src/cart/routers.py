from typing import Annotated
from fastapi import Depends, routing
from fastapi import HTTPException
from auth.auth import UserInDB, get_current_user
from cart.models import Cart
from conn.conn import connect_to_db

router = routing.APIRouter()


# Формирование корзины
@router.post("/cart")
async def add_product_cart(cart: Cart, current_user: Annotated[UserInDB,
                        Depends(get_current_user)]):
    if cart.acc_id != current_user.id or await current_user.get_role() != "admin":
        raise HTTPException(500, "id пользоваьеля не совпадает")
    conn = await connect_to_db()

    # Проверка наличия товара в базе данных
    query = "SELECT * FROM product WHERE id = $1"
    product = await conn.fetchrow(query, cart.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Создание
    query = """INSERT INTO product_in_cart (acc_id, product, quantity)
            VALUES ($1, $2, $3) RETURNING id"""
    product_id = await conn.fetchval(query, cart.acc_id,
                                    cart.product_id, cart.quantity)

    # Получение созданного заказа
    query = "SELECT * FROM product_in_cart WHERE id = $1"
    created_cart = await conn.fetchrow(query,product_id)

    await conn.close()

    return created_cart

# @router.put("/refresh")
# async def refresh_cart(user_id: int):
#     conn = await connect_to_db()
#  
#     sql_query = f"SELECT * FROM product_in_cart WHERE acc_id = {user_id}"

#     # Выполнение запроса SQL
#     result = await conn.fetch(sql_query)

#     # Закрытие соединения с базой данных
#     await conn.close()

#     # Проверка, что корзина не пустая
#     if not result:
#         raise ValueError("Корзина пользователя пуста")

#     # Получение списка всех продуктов
#     conn = await connect_to_db()
#     all_products = f"SELECT * FROM product WHERE id = {id}"
#     await conn.close()


#     # Получение списка продуктов, которых нет в корзине
#   missing_products = list(set(all_products) - set([row["product"] for row in result]))

#     # Возвращение списка недостающих продуктов в качестве ответа
#     return {"missing_products": missing_products}
