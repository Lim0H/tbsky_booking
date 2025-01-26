import importlib
import importlib.util
import os
import sys
from typing import Optional

import asyncclick

COMMANDS_FOLDER = os.path.join(os.path.dirname(__file__))


class CliManager(asyncclick.Group):
    def list_commands(self, ctx: asyncclick.Context) -> list[str]:
        lst_commands = super().list_commands(ctx)

        lst_commands_group = list(
            filter(
                lambda f: all(
                    (
                        os.path.isdir(os.path.join(COMMANDS_FOLDER, f)),
                        not f.startswith("__"),
                        not f.endswith("__"),
                    )
                ),
                os.listdir(COMMANDS_FOLDER),
            )
        )
        return lst_commands + sorted(lst_commands_group)

    def get_command(
        self, ctx: asyncclick.Context, name: str
    ) -> Optional[asyncclick.Command]:
        file_path = os.path.join(COMMANDS_FOLDER, name, "__init__.py")
        if not os.path.exists(file_path):
            return super().get_command(ctx, name)

        spec = importlib.util.spec_from_file_location("cli_group", file_path)
        if spec is None:
            raise ValueError

        cli_group = importlib.util.module_from_spec(spec)
        sys.modules["cli_group"] = cli_group
        if spec.loader is None:
            raise ValueError

        spec.loader.exec_module(cli_group)
        cli: asyncclick.Group = cli_group.cli
        return cli

    def command(self, *args, **kwargs):
        default_command = kwargs.pop("default_command", False)

        if default_command and not args:
            kwargs["name"] = kwargs.get("name", "<DEFAULT COMMAND>")

        decorator = super(CliManager, self).command(*args, **kwargs)

        if default_command:

            def new_decorator(f):
                cmd = decorator(f)
                self.default_command = cmd.name
                return cmd

            return new_decorator

        return decorator

    def resolve_command(self, ctx: asyncclick.Context, args: list[str]):
        try:
            return super(CliManager, self).resolve_command(ctx, args)
        except asyncclick.UsageError:
            args.insert(0, self.default_command)
            return super(CliManager, self).resolve_command(ctx, args)
