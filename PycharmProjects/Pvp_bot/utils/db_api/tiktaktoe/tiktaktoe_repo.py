from aiogram.types import user
from asyncpg.connection import Connection

class TikTakToeRepo:
    def __init__(self, conn: Connection):
        self.conn = conn
    

    async def get_lobby_players(self, rates_id):
        sql = 'select * from "tiktaktoe_lobby" where rates_id = $1'
        res = await self.conn.fetch(sql, rates_id)
        return res
    
    async def create_game(self, rates_id:int , first_step_user_id:int ):
        sql = 'insert into "tiktaktoe_game"("rates_id","user_step_id") values($1,$2) on conflict do nothing returning id'
        id = await self.conn.fetchrow(sql, rates_id, first_step_user_id)
        if id:
            return id['id']
        
    
    async def delete_users_lobby(self, user_id:int):
        sql = 'delete from "tiktaktoe_lobby" where user_id = $1'
        id = await self.conn.fetch(sql, user_id)
        return id
    
    async def add_user_to_game(self, user_id:int, game_id:int, character: str):
        sql = 'insert into "tiktaktoe_game_user"("user_id","game_id", "character") values($1, $2, $3) on conflict do nothing'
        id = await self.conn.execute(sql, user_id, game_id, character)
    
    async def set_game_user_step(self, sequence:int, user_step_id:int, game_id: int):
        sql = 'update "tiktaktoe_game" set step = $1 and user_step_id = $2 where game_id = $3'
        id = await self.conn.execute(sql, sequence, user_step_id, game_id)
    

    async def create_cells(self, n:int, game_id: int):
        sql = 'insert into "tiktaktoe_cell"("game_id") values($1) on conflict do nothing'
        for i in range(0, n):
            await self.conn.execute(sql, game_id)

    async def add_user_steps(self, n:int, game_id: int, user_ids:list):
        sql = ""
        for i in range(1, n+1):
            user_id = user_ids.pop(0)
            sql += f'insert into "tiktaktoe_user_step"("sequence", "user_id","game_id") values({i},{user_id},{game_id}) on conflict do nothing;'
            user_ids.append(user_id)
        await self.conn.execute(sql)
    
    async def get_step(self, game_id: int, sequence: int):
        sql = """select * from "tiktaktoe_user_step" where game_id = $1 and sequence = $2 """
        
        return await self.conn.fetchrow(sql, game_id, sequence)

    
    async def get_game_cells(self, game_id: int):
        sql = 'select * from tiktaktoe_cell where game_id = $1'
        res = await self.conn.fetch(sql, game_id)
        return res
    
    async def get_game_cell_by_id(self, id: int):
        sql = 'select * from tiktaktoe_cell where id = $1'
        res = await self.conn.fetchrow(sql, id)
        return res
    
    async def get_game_by_id(self, id: int):
        sql = 'select * from tiktaktoe_game where id = $1'
        res = await self.conn.fetchrow(sql, id)
        return res

    async def get_game_user(self, user_id: int, game_id: int):
        sql = 'select * from tiktaktoe_game_user where game_id = $1 and user_id = $2'
        return await self.conn.fetchrow(sql, game_id, user_id)
    
    async def get_game_users(self, game_id: int):
        sql = 'select * from tiktaktoe_game_user where game_id = $1'
        return await self.conn.fetch(sql, game_id)
    

    async def set_game_user_message_id(self, user_id: int, game_id: int, message_id):
        sql = 'update tiktaktoe_game_user set message_id = $1 where game_id = $2 and user_id = $3'
        return await self.conn.execute(sql, game_id, user_id, message_id)

    async def add_lobby_user(self, user_id: int, rates_id: int):
        sql = 'insert into "tiktaktoe_lobby"("user_id","rates_id") values($1, $2) on conflict do nothing'
        await self.conn.execute(sql, user_id, rates_id)
    
    async def take_cell(self, user_id: int, cell_id: int):
        sql = 'update "tiktaktoe_cell" set user_id = $1 and is_busy=true where id = $2'
        await self.conn.execute(sql, user_id, cell_id)

    

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