from tbsky_booking.commands import run_cli_manager
from tbsky_booking.core import init_logging


def main():
    init_logging()
    run_cli_manager(_anyio_backend="asyncio")
