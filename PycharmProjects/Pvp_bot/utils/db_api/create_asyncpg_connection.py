from asyncpg import connect

async def create_conn(conn_str: str):
    conn_str = "postgres://postgres:123123123@144.91.110.3:5432/postgres"
    #conn_str = "postgres://postgres:jwnPbVr263Dk@localhost:5432/PvP_bot_db"
    return await connect(conn_str)