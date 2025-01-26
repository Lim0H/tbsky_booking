import asyncclick

from tbsky_booking.core import initialize_database as init_db


@asyncclick.group("Database  commands")
def db_cli():
    pass


@db_cli.command()
async def initialize_database():
    await init_db()
