import asyncclick

from .fill_repositories import fill_repositories_cli

__all__ = ["cli"]
cli = asyncclick.CommandCollection(sources=[fill_repositories_cli])
