from typing import Annotated, List
from asyncpg import Connection
from fastapi import Depends, HTTPException, routing
from auth.auth import UserInDB, get_current_user
from conn.conn import connect_to_db
from order.models import ProductInCart, ProductOrder
from role.models import Role


router = routing.APIRouter()


@router.post("/role")
async def add_role(role: Role, current_user: Annotated[UserInDB, Depends(get_current_user)]):
    if not await current_user.is_admin_or_moder():
        raise HTTPException(500, "недостаточно прав")
    # await db.check_role(role) 
# получаем от пользователя обьект класса Role ( в нем акк_айди , имя роли которую хотим дать)



# написать такой инстер который в табличку акк_роль будет добавлять новую запись с ролью пользователя

@router.post("/add_new_role")
async def add_new_role(acc_id, role):
    conn = await connect_to_db()
    try:
        query = "INSERT INTO acc_role (acc_id, role) VALUES ($1, $2)"
        await conn.execute(query, int(acc_id), role)
    except Exception as error:
        print(repr(error))
    finally:
        await conn.close()
