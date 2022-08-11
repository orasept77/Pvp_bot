from asyncpg import connect

from data.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME


async def return_connection_string():
    return f"postgres://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


async def create_conn():
    conn_str = await return_connection_string()
    return await connect(conn_str)

