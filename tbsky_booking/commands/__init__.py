import asyncclick
from tbsky_booking.api import run_fastapi_server

from .cli_manager import CliManager
from .flights import *


@asyncclick.group(
    cls=CliManager, help="TBSky Booking commands", invoke_without_command=True
)
@asyncclick.pass_context
async def run_cli_manager(ctx: asyncclick.Context):
    if ctx.invoked_subcommand is None:
        await run_fastapi_server()
