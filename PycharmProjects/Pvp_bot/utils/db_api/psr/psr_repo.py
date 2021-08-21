from asyncpg.connection import Connection

class PSRRepo:
    def __init__(self, conn: Connection):
        self.conn = conn



    async def add_lobby_user(self, user_id: int, rates_id: int, user_count):
        sql = 'insert into "psr_lobby"("user_id","rates_id", "user_count") values($1, $2, $3) on conflict do nothing'
        await self.conn.execute(sql, user_id, rates_id, user_count)

    async def create_game(self, rates_id:int , user_count:int, game_type_id ):
        sql = 'insert into "psr"("rates_id", "user_count", "game_type_id") values($1,$2,$3) on conflict do nothing returning id'
        id = await self.conn.fetchrow(sql, rates_id, user_count, game_type_id)
        if id:
            return id['id']


    async def add_user_to_game(self, user_id:int, game_id:int):
        sql = 'insert into "psr_user"("user_id","psr_id") values($1, $2) on conflict do nothing'
        id = await self.conn.execute(sql, user_id, game_id)

    async def get_lobby_players(self, rates_id, user_count):
        sql = 'select * from "psr_lobby" where rates_id = $1 and user_count = $2 '
        res = await self.conn.fetch(sql, rates_id, user_count)
        return res
    
    async def add_round(self, game_id: int, sequence:int):
        sql = 'insert into "psr_round"("psr_id", "sequence") values($1, $2) on conflict do nothing returning id '
        res = await self.conn.fetchrow(sql, game_id, sequence)
        return res

    async def delete_users_lobby(self, user_id:int):
        sql = 'delete from "psr_lobby" where user_id = $1'
        await self.conn.execute(sql, user_id)

    async def set_game_end(self, game_id:int):
        sql = 'update "psr" set is_end = true where id = $1'
        await self.conn.execute(sql, game_id)



    async def get_variants(self, game_type_id):
        sql = 'select * from "psr_variant" where game_type_id = $1 '
        res = await self.conn.fetch(sql, game_type_id)
        return res

    async def set_game_user_message_id(self, user_id: int, game_id: int, message_id):
        sql = 'update psr_user set message_id = $1 where psr_id = $2 and user_id = $3'
        return await self.conn.execute(sql, message_id, game_id, user_id)
    

    async def get_game_types(self):
        sql = 'select * from "psr_game_type"'
        res = await self.conn.fetch(sql)
        return res
    



    

        
    
    
    
    
    async def set_game_user_step(self, sequence:int, user_step_id:int, game_id: int):
        sql = 'update "tiktaktoe_game" set step = $1 , user_step_id = $2 where id = $3'
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
        sql = 'select * from tiktaktoe_cell where game_id = $1 order by id '
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
    

    

    
    
    async def take_cell(self, user_id: int, cell_id: int):
        sql = 'update "tiktaktoe_cell" set user_id = $1 , is_busy=true where id = $2'
        await self.conn.execute(sql, user_id, cell_id)
