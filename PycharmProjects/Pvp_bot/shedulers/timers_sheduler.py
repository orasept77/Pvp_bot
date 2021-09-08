from apscheduler.triggers.interval import IntervalTrigger

from handlers.users.blackjack.blackjack_autolose import blackjack_player_auto_loose
from utils.db_api.blackjack.blackjack_repo import BlackJackRepo
from utils.db_api.create_asyncpg_connection import create_conn


class TimerRepository:
    def __init__(self, scheduler, timer_name=None, user_id=None, game_id=None):
        self.scheduler = scheduler
        self.timer_name = timer_name
        self.user_id = user_id
        self.game_id = game_id

        # Переменная, где хранится функция для работы с ней
        self.job = None

        # Как часто обновлять таймер. Для модификации - измените аттрибут "tick"
        # Один раз в <tick> будет срабатывать функция для обновления таймера и таймер будет уменьшаться на <tick>
        # Чем число меньше - тем больше памяти требуется
        self.tick = 5
        self.intervalTrigger = IntervalTrigger(seconds=self.tick)

        # Стандартное время таймера
        self.default_time = 90  # seconds

        # Далее локальные переменные
        # Стандартное время на ход для каждой игры. Для кастомизации - изменить после "="
        # Переменные имеют формат "self.default_<timer_name>_time = self.default_time"
        self.default_blackjack_time = self.default_time
        self.default_tiktaktoe_time = self.default_time
        self.default_rps_time = self.default_time

        # Переменные в которых ведётся отсчёт
        # Переменные имеют формат "self.<timer_name>_time_left = self.default_<timer_name>_time"
        self.blackjack_time_left = self.default_blackjack_time
        self.tiktaktoe_time_left = self.default_tiktaktoe_time
        self.rps_time_left = self.default_rps_time

    # Делает тик для указанного таймера. Тут следует писать логику отсчёта тика для новый имён таймеров
    async def timer_make_tick(self):
        # Для каждого нового имени таймера следует добавить новый IF с подобной логикой по примеру ниже
        # if self.timer_name == '<timer_name>':
        #     self.<timer_name>_time_left -= self.tick
        #     if self.<timer_name>_time_left <= 0:
        #         do_something()

        # Логика автолуза Блекджека
        if self.timer_name == 'blackjack':
            self.blackjack_time_left -= self.tick
            if self.blackjack_time_left == 0:
                conn = await create_conn("conn_str")
                repo = BlackJackRepo(conn=conn)
                game = repo.get_game(self.game_id)
                if game is None:
                    pass
                else:
                    await blackjack_player_auto_loose(int(self.user_id))
                if self.job is None:
                    pass
                else:
                    self.job.remove()
                await conn.close()

        # Логика автолуза Крестиков-Ноликов
        if self.timer_name == 'tiktaktoe':
            self.tiktaktoe_time_left -= self.tick
            if self.tiktaktoe_time_left <= 0:
                # !-- Функция автолуза для игрока --!
                self.job.remove()

        # Логика автолуза Камень-Ножницы-Бумага
        if self.timer_name == 'rpc':
            self.rps_time_left -= self.tick
            if self.rps_time_left <= 0:
                # !-- Функция автолуза для игрока --!
                self.job.remove()

    # !-- Новый код писать ниже --!

    # Код пиши тут

    # !-- Функции ниже не изменять --!

    # Функции для управления таймером:
    # start_timer   -   Функция старта таймера. Запускает таймер в формате
    # update_timer  -   Восстанавливает указанный таймер к стандартному значению, указанному в
    # pause_timer   -   Ставит указанный таймер на паузу
    # resume_timer  -   Снимает паузу с указанного таймера
    # remove_timer  -   Удаляет указанный таймер из планировщика
    async def start_timer(self):
        if self.user_id is None:
            self.job = self.scheduler.add_job(self.timer_make_tick, self.intervalTrigger,
                                              id=f'{self.timer_name}_timer')
        else:
            self.job = self.scheduler.add_job(self.timer_make_tick, self.intervalTrigger,
                                              id=f'{self.timer_name}_timer_{self.user_id}_{self.game_id}')

    async def update_timer(self):
        if self.user_id is None:
            self.scheduler.remove_job(f'{self.timer_name}_timer')
            self.job = self.scheduler.add_job(self.timer_make_tick, self.intervalTrigger,
                                              id=f'{self.timer_name}_timer')
        else:
            self.scheduler.remove_job(f'{self.timer_name}_timer_{self.user_id}_{self.game_id}')
            self.job = self.scheduler.add_job(self.timer_make_tick, self.intervalTrigger,
                                              id=f'{self.timer_name}_timer_{self.user_id}_{self.game_id}')

    async def pause_timer(self):
        if self.user_id is None:
            self.scheduler.pause_job(f'{self.timer_name}_timer')
        else:
            self.scheduler.pause_job(f'{self.timer_name}_timer_{self.user_id}_{self.game_id}')

    async def resume_timer(self):
        if self.user_id is None:
            self.scheduler.resume_job(f'{self.timer_name}_timer')
        else:
            self.scheduler.resume_job(f'{self.timer_name}_timer_{self.user_id}_{self.game_id}')

    async def remove_timer(self):
        if self.user_id is None:
            self.scheduler.remove_job(f'{self.timer_name}_timer')
        else:
            self.scheduler.remove_job(f'{self.timer_name}_timer_{self.user_id}_{self.game_id}')
