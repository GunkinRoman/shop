from auth.models import UserForReg
import asyncpg


class AuthRepo:
    async def save_new_user(self, user: UserForReg):
        conn = await asyncpg.connect("postgresql://social_network_user:social_network_user_password123@project-main_pg_db:5432/social_network_db")
        await conn.execute(
            """
        INSERT INTO account (
            username, first_name,last_name, passw, mail, mobile_telephone, address
        ) VALUES ($1, $2, $3, $4, $5, $6, $7)
        """,
            user.username,
            user.first_name,
            user.last_name,
            user.passw,
            user.mail,
            user.mobile_telephone,
            user.address,
        )

        await conn.close()

    async def check_username_passw(self, username: str, passw: str) -> bool:
        conn = await asyncpg.connect("postgresql://social_network_user:social_network_user_password123@project-main_pg_db:5432/social_network_db")
        row = await conn.fetchrow(
            "SELECT * FROM account WHERE username = $1 AND passw = $2", username, passw
        )
        if row:
            return True
        else:
            return False


db = AuthRepo()
