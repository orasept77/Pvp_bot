from aiogram.types import user
from asyncpg.connection import Connection

class TikTakToeRepo:
    def __init__(self, conn: Connection):
        self.conn = conn
    

    async def get_lobby_players(self, rates_id, user_id):
        sql = 'select u.* from "tiktaktoe_lobby" tl join "users" u on u."id" = tl."user_id" where rates_id = $1 and user_id != $2'
        res = await self.conn.fetch(sql, rates_id, user_id)
        return res
    
    async def create_game(self, rates_id:int , first_step_user_id:int, private_lobby_id):
        sql = 'insert into "tiktaktoe_game"("rates_id","user_step_id", "private_lobby_id") values($1,$2,$3) on conflict do nothing returning id'
        id = await self.conn.fetchrow(sql, rates_id, first_step_user_id, private_lobby_id)
        if id:
            return id['id']
        
    async def create_game_round(self, game_id:int , first_step_user_id:int, sequence: int = 1):
        sql = 'insert into "tiktaktoe_round"("game_id","user_step_id", "sequence") values($1,$2,$3) on conflict do nothing returning id'
        id = await self.conn.fetchrow(sql, game_id, first_step_user_id, sequence)
        if id:
            return id['id']
    
    async def set_game_end(self, game_id:int):
        sql = 'update "tiktaktoe_game" set is_end = true where id = $1'
        await self.conn.execute(sql, game_id)
    
    async def set_round_end(self, round_id:int):
        sql = 'update "tiktaktoe_round" set is_end = true where id = $1'
        await self.conn.execute(sql, round_id)
        
    
    async def delete_users_lobby(self, user_id:int):
        sql = 'delete from "tiktaktoe_lobby" where user_id = $1'
        id = await self.conn.fetch(sql, user_id)
        return id
    
    async def add_user_to_game(self, user_id:int, game_id:int, character: str):
        sql = 'insert into "tiktaktoe_game_user"("user_id","game_id", "character") values($1, $2, $3) on conflict do nothing'
        id = await self.conn.execute(sql, user_id, game_id, character)
    
    async def add_user_to_round(self, user_id:int, round_id:int, character: str):
        sql = 'insert into "tiktaktoe_round_user"("user_id","round_id", "character") values($1, $2, $3)'
        id = await self.conn.execute(sql, user_id, round_id, character)

    async def set_game_round_user_step(self, sequence:int, user_step_id:int, round_id: int):
        sql = 'update "tiktaktoe_round" set step = $1 , user_step_id = $2 where id = $3'
        id = await self.conn.execute(sql, sequence, user_step_id, round_id)
    
    async def set_round_winner_id(self, winner_id:int, round_id: int):
        sql = 'update "tiktaktoe_round" set winner_id = $1 where id = $2'
        id = await self.conn.execute(sql, winner_id, round_id)
    

    async def get_round_winners(self, winner_id, game_id: int):
        sql = 'select * from "tiktaktoe_round" where winner_id = $1 and game_id = $2'
        res = await self.conn.fetch(sql, winner_id, game_id)
        return res

    

    async def create_cells(self, n:int, round_id: int):
        sql = 'insert into "tiktaktoe_cell"("round_id") values($1) on conflict do nothing'
        for i in range(0, n):
            await self.conn.execute(sql, round_id)

    async def add_user_steps(self, n:int, round_id: int, user_ids:list):
        sql = ""
        for i in range(1, n+1):
            user_id = user_ids.pop(0)
            sql += f'insert into "tiktaktoe_user_step"("sequence", "user_id","round_id") values({i},{user_id},{round_id}) on conflict do nothing;'
            user_ids.append(user_id)
        await self.conn.execute(sql)
    
    async def get_step(self, round_id: int, sequence: int):
        sql = """select * from "tiktaktoe_user_step" where round_id = $1 and sequence = $2 """
        
        return await self.conn.fetchrow(sql, round_id, sequence)

    
    async def get_game_cells(self, round_id: int):
        sql = 'select * from tiktaktoe_cell where round_id = $1 order by id '
        res = await self.conn.fetch(sql, round_id)
        return res
    
    async def get_round_cell_by_id(self, id: int):
        sql = 'select * from tiktaktoe_cell where id = $1'
        res = await self.conn.fetchrow(sql, id)
        return res
    
    async def get_game_by_id(self, id: int):
        sql = 'select * from tiktaktoe_game where id = $1'
        res = await self.conn.fetchrow(sql, id)
        return res
    

    async def get_round_by_id(self, id: int):
        sql = 'select * from tiktaktoe_round where id = $1'
        res = await self.conn.fetchrow(sql, id)
        return res

    async def get_game_user(self, user_id: int, game_id: int):
        sql = 'select * from tiktaktoe_game_user where game_id = $1 and user_id = $2'
        return await self.conn.fetchrow(sql, game_id, user_id)
    
    async def get_round_users(self, round_id: int):
        sql = 'select u.*, tr."character", tr."message_id" from tiktaktoe_round_user tr join users u on u."id" = tr."user_id" where round_id = $1'
        return await self.conn.fetch(sql, round_id)
    
    async def get_game_users(self, game_id: int):
        sql = 'select * from tiktaktoe_game_user where game_id = $1'
        return await self.conn.fetch(sql, game_id)
    

    async def set_game_round_user_message_id(self, user_id: int, round_id: int, message_id):
        sql = 'update tiktaktoe_round_user set message_id = $1 where round_id = $2 and user_id = $3'
        return await self.conn.execute(sql, message_id, round_id, user_id)

    async def add_lobby_user(self, user_id: int, rates_id: int):
        sql = 'insert into "tiktaktoe_lobby"("user_id","rates_id") values($1, $2) on conflict do nothing'
        await self.conn.execute(sql, user_id, rates_id)
    
    async def take_cell(self, user_id: int, cell_id: int):
        sql = 'update "tiktaktoe_cell" set user_id = $1 , is_busy=true where id = $2'
        await self.conn.execute(sql, user_id, cell_id)

    async def create_private_lobby(self, rates_id: int):
        sql = 'insert into "tiktaktoe_lobby_private"("rates_id") values($1) on conflict do nothing returning id'
        id = await self.conn.fetchrow(sql, rates_id)
        if id:
            return id['id']

    async def get_private_lobby(self, lobby_id):
        sql = 'select * from "tiktaktoe_lobby_private" where id = $1'
        res = await self.conn.fetchrow(sql, lobby_id)
        return res
    
    async def get_lobby_private_players(self, lobby_id):
        sql = 'select u.* from "tiktaktoe_lobby_private_user" tlpu join users u on u."id" = tlpu."user_id" where lobby_id = $1'
        res = await self.conn.fetch(sql, lobby_id)
        return res
    
    async def add_private_lobby_user(self, lobby_id: int, user_id: int):
        sql = 'insert into "tiktaktoe_lobby_private_user"("lobby_id", "user_id") values($1, $2) on conflict do nothing'
        id = await self.conn.fetchrow(sql, lobby_id, user_id)
        if id:
            return id['id']
        
    async def delete_private_lobby_user(self, lobby_id: int, user_id: int):
        sql = 'delete from "tiktaktoe_lobby_private_user" where "lobby_id" = $1 and "user_id" = $2'
        id = await self.conn.execute(sql, lobby_id, user_id)

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
