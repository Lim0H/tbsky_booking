import asyncclick

from .database import db_cli

__all__ = ["cli"]
cli = asyncclick.CommandCollection(sources=[db_cli])
