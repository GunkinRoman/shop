import asyncpg


async def connect_to_db():
    conn = await asyncpg.connect(
        "postgresql://social_network_user:social_network_user_password123@project-main_pg_db:5432/social_network_db")
    return conn