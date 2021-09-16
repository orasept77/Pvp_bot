from utils.db_api.create_asyncpg_connection import create_conn

async def create_tables_if_not_exists():
    connection = await create_conn()
    try:
        query = """
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            first_name varchar(255) NULL,
            username varchar(255),
            last_name varchar(255) NULL
        )"""
        await connection.fetch(query)

        query = """
        CREATE TABLE IF NOT EXISTS deposits(
            id SERIAL PRIMARY KEY,
            user_id int,
            balance integer DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )"""
        await connection.fetch(query)

        query = """
        CREATE TABLE IF NOT EXISTS statistics(
            user_id int,
            games_blackjack integer DEFAULT 0,
            win_blackjack integer DEFAULT 0,
            games_tiktaktoe integer DEFAULT 0,
            win_tiktaktoe integer DEFAULT 0,
            games_rpc integer DEFAULT 0,
            win_rpc integer DEFAULT 0,
            win_balance integer DEFAULT 0,
            lost_balance integer DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )"""
        await connection.fetch(query)

        query = """
        CREATE TABLE IF NOT EXISTS rates(
            id SERIAL PRIMARY KEY,
            value INTEGER
        )"""
        await connection.fetch(query)

        query = """
         CREATE TABLE IF NOT EXISTS blackjack_lobby(
            user_id BIGINT,
            rates_id INTEGER,
            chat_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (rates_id) REFERENCES rates(id)
        )"""
        await connection.fetch(query)

        query = """
        CREATE TABLE IF NOT EXISTS blackjack_invite_lobby(
            id SERIAL PRIMARY KEY,
            user_id BIGINT,
            rates_id INTEGER,
            chat_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (rates_id) REFERENCES rates(id)
        )"""
        await connection.fetch(query)

        query = """
        CREATE TABLE IF NOT EXISTS blackjack_game(
            id SERIAL PRIMARY KEY,
            rates_id INTEGER,
            user_turn INTEGER,
            result varchar(15) DEFAULT NULL,
            deck JSON DEFAULT '[]',
            game_round INTEGER DEFAULT 1,
            is_end varchar(10) NULL,
            FOREIGN KEY (rates_id) REFERENCES rates(id),
            FOREIGN KEY (user_turn) REFERENCES users(id)
        )"""
        await connection.fetch(query)

        query = """
        CREATE TABLE IF NOT EXISTS blackjack_game_user(
            user_id INTEGER,
            game_id INTEGER,
            chat_id INTEGER,
            message_id INTEGER,
            hand JSON DEFAULT '[]',
            state varchar(10) DEFAULT 'NONE',
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (game_id) REFERENCES blackjack_game(id)
        )"""
        await connection.fetch(query)

        query = """
        CREATE TABLE IF NOT EXISTS blackjack_game_dealer(
            game_id int,
            hand JSON DEFAULT '[]',
            FOREIGN KEY (game_id) REFERENCES blackjack_game(id)
        )"""
        await connection.fetch(query)

        query = """
        CREATE TABLE IF NOT EXISTS liqpay_deposits(
            id SERIAL PRIMARY KEY,
            user_id INTEGER,
            amount INTEGER DEFAULT 0,
            phone varchar(20) DEFAULT 'NONE',
            state varchar(20) DEFAULT 'NONE',
            FOREIGN KEY (user_id) REFERENCES users(id)
        )"""
        await connection.fetch(query)

        query = """
        CREATE TABLE IF NOT EXISTS liqpay_withdrawals(
            id SERIAL PRIMARY KEY,
            user_id INTEGER,
            payment_type varchar(20) DEFAULT 'NONE',
            amount INTEGER DEFAULT 0,
            ip varchar(20) DEFAULT 'NONE',
            card_number varchar(40) DEFAULT 'NONE',
            phone varchar(20) DEFAULT 'NONE',
            email varchar(255) DEFAULT 'NONE',
            first_name varchar(50) DEFAULT 'NONE',
            last_name varchar(50) DEFAULT 'NONE',
            state varchar(20) DEFAULT 'NONE',
            FOREIGN KEY (user_id) REFERENCES users(id)
        )"""
        await connection.fetch(query)

        query = """TRUNCATE blackjack_game_user, blackjack_game, blackjack_invite_lobby, blackjack_lobby, blackjack_game_dealer"""
        res = await connection.fetch(query)

        print("[OK!] - База данных успешно создана и обновленна!")
        return res
    except:
        print("[ERROR!] - Ошибка при создании базы")
    await connection.close()
