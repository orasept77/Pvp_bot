from asyncpg.connection import Connection


class TikTakToeRepo:
    def __init__(self, conn: Connection):
        self.conn = conn

    async def get_lobby_players(self, rates_id):
        sql = 'select * from "tiktaktoe_lobby" where rates_id = $1'
        res = await self.conn.fetch(sql, rates_id)
        return res

    async def create_game(self, rates_id: int, first_step_user_id: int):
        sql = 'insert into "tiktaktoe_game"("rates_id","user_step_id") values($1,$2) on conflict do nothing returning id'
        id = await self.conn.fetch(sql, rates_id)
        return id

    async def delete_users_lobby(self, user_id: int):
        sql = 'delete form "tiktaktoe_lobby" where user_id = $1'
        id = await self.conn.fetch(sql, user_id)
        return id

    async def add_user_to_game(self, user_id: int, game_id: int, character: str):
        sql = 'insert into "tiktaktoe_game_user"("user_id","game_id", "character") values($1, $2, $3) on conflict do nothing'
        id = await self.conn.execute(sql, user_id)

    async def create_cells(self, n: int, game_id: int):
        sql = 'insert into "tiktaktoe_cell"(,"game_id") values($1, $2) on conflict do nothing'
        for i in range(0, n):
            await self.conn.execute(sql, game_id)

    async def get_game_cell(self, game_id: int):
        sql = 'select * from tiktaktoe_cell where game_id = $1'
        res = await self.conn.fetch(sql, game_id)
        return res

    async def get_user_character(self, user_id: int, game_id: int):
        sql = 'select * from tiktaktoe_game_user where game_id = $1 and user_id = $2'
        return await self.conn.fetchrow(sql, game_id, user_id)

    """async def get_user(self, user_id):
        sql = 'select * from "User" where "Id" = $1'
        user = await self.conn.fetchrow(sql, user_id)
        if user:
            return User(**user)
    async def create_user(self, user_id, username):
        sql = insert into "User"("Id","UserName") values($1,$2) on conflict do nothing returning * 
        res = await self.conn.fetchrow(sql, user_id, username)
        if res:
            return User(**res)
    async def get_user_groups(self, user_id):
        sql =  select * from "UserGroup"  where "UserId" = $1 ORDER BY "UserId" 
        groups = await self.conn.fetch(sql, user_id)
        if len(groups) > 0:
            return [UserGroup(**group) for group in groups]
        return groups

    async def set_off_notification(self, user_id, status):
        sql =  update "User" set "OffNotifications" = $2 where "Id" = $1 
        await self.conn.execute(sql, user_id, status)"""