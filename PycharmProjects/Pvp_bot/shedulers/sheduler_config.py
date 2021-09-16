import sqlalchemy
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Database URL to connect
from data.config import MAX_INSTANCES, TIMEZONE
from utils.db_api.create_asyncpg_connection import return_connection_string


class SchedulerRepo:
    def __init__(self):
        # Максимально количество выполняемых задач одновременно
        self.max_instances = MAX_INSTANCES
        # Timezone
        self.timezone = TIMEZONE
        # Ссылка на базу данных
        #self.database_url = await return_connection_string()

        self.scheduler = None

    def start_scheduler(self):
        self.scheduler = AsyncIOScheduler({
            # 'apscheduler.jobstores.default': {
            #     'type': 'sqlalchemy',
            #     'url': 'sqlite:///jobs.sqlite'
            # },
            'apscheduler.job_defaults.coalesce': 'false',
            'apscheduler.job_defaults.max_instances': f'{str(self.max_instances)}',
            'apscheduler.timezone': f'{str(self.timezone)}',
        })

    def return_scheduler(self):
        return self.scheduler