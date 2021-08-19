from utils.db_api.close_connection import close_connection
from utils.db_api.create_connection import db_connection
from utils.db_api.execute_query import execute_query

query = """

CREATE TABLE IF NOT EXISTS users(
    id INT PRIMARY KEY,
    name varchar(255) NULL,
    username varchar(255)
);

CREATE TABLE IF NOT EXISTS deposits(
    id SERIAL PRIMARY KEY,
    user_id int,
    balance integer DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS rooms(
    id SERIAL PRIMARY KEY,
    player_one INT NOT NULL,
    player_two INT NULL,
    timeout integer DEFAULT 300,
    room_state varchar(20) DEFAULT 'WAITING',
    FOREIGN KEY (player_one) REFERENCES users(id),
    FOREIGN KEY (player_two) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS blackjacks(
    id SERIAL PRIMARY KEY,
    room_id INT,
    deck varchar(255) NULL,
    hand_player_one varchar(255) NULL,
    hand_player_two varchar(255) NULL,
    hand_dealer varchar(255) NULL,
    game_round integer DEFAULT 1,
    game_result varchar(50),
    FOREIGN KEY (room_id) REFERENCES rooms(id)
);

"""


def create_tables_if_not_exists():
    connection = db_connection()
    try:
        execute_query(connection, query)
        print("База данных успешно создана")
    except:
        print("Ошибка при создании базы")
    close_connection(connection)
