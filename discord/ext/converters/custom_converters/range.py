from __future__ import annotations

import inspect

try:
    from types import GenericAlias
except ImportError:
    from typing import _GenericAlias as GenericAlias

import fishhook
from typing_extensions import get_args
from discord.ext.commands import Context, BadArgument

from ..converter import CustomConverter


@fishhook.hook(range)
def __class_getitem__(cls: type[range], args: tuple[int, ...]) -> GenericAlias:
    return GenericAlias(cls, args if isinstance(args, tuple) else (args,))


class InRangeConverter(CustomConverter[range]):
    async def convert(self, ctx: Context, argument: str) -> int:
        try:
            param: inspect.Parameter = inspect.currentframe().f_back.f_locals["param"]
        except KeyError:
            raise TypeError(f"{self.__class__.__name__} cannot be used manually.") from None

        value = range(*get_args(param.annotation))

        try:
            argument = int(argument)
        except ValueError:
            raise BadArgument(f"{argument} is not int")

        if argument in value:
            return argument
        raise BadArgument(f"{argument} not in range")
