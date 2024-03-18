import peewee
from configs.env import (
    DATABASE_NAME,
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_HOST,
    DATABASE_PORT,
)
from playhouse.pool import PooledPostgresqlExtDatabase
from contextvars import ContextVar
import logging
import time
from functools import wraps
from configs.env import APP_ENV, ENVIRONMENT_TYPE

logger = logging.getLogger("peewee")
db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())


class PeeweeConnectionState(peewee._ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter_ns()
        ret = func(*args, **kwargs)
        end_time = time.perf_counter_ns()
        elapsed_time_ms = (end_time - start_time) / 1e6
        logger.info("Execution Time: %.2f ms" % elapsed_time_ms)
        return ret

    return wrapper


db_params = {
    "database": DATABASE_NAME,
    "user": DATABASE_USER,
    "password": DATABASE_PASSWORD,
    "host": DATABASE_HOST,
    "port": DATABASE_PORT,
    "autorollback": True,
    "max_connections": 100,
}


class CustomDatabase(PooledPostgresqlExtDatabase):
    @timer
    def execute_sql(self, sql, params=None):
        return super().execute_sql(sql, params)


db = (
    CustomDatabase(**db_params)
    if ENVIRONMENT_TYPE == 'cli' and APP_ENV != 'production'
    else PooledPostgresqlExtDatabase(**db_params)
)

db._state = PeeweeConnectionState()
